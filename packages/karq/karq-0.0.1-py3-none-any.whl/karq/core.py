from asyncio import (
    AbstractEventLoop,
    CancelledError,
    Event,
    Future,
    get_event_loop,
    sleep,
)
from contextlib import suppress
from dataclasses import field
from functools import partial, wraps
from random import randint
from ssl import SSLContext
from time import time
from typing import Any, ClassVar

import aiormq.exceptions as rmq
import pamqp.commands as cmd
import pamqp.exceptions as pam
from aio_pika import Connection as DumbConnection
from aio_pika import DeliveryMode, Message
from aio_pika.abc import ExchangeType
from aio_pika.connection import make_url
from aio_pika.tools import CallbackCollection
from aiormq.abc import DeliveredMessage
from fair_async_rlock import FairAsyncRLock
from kalib import (
    HTTP,
    Is,
    Logging,
    Property,
    Str,
    Who,
    dataclass,
    dumps,
    json,
    loads,
    unique,
)
from xxhash import xxh32_hexdigest
from xxhash import xxh128_hexdigest as digest

import karq.exceptions as exc
from karq.retry import TimeoutExceptions, retry
from karq.utils import attach, log_long_wait

__all__ = ('Rabbit', 'Routine', 'Timeouts')


class Tag(dataclass.mutable):

    _tag: str | None = None

    @classmethod
    def new(cls, *args, **kw):
        return cls.load(kw, *args)

    def __bool__(self):
        return bool(self._tag)

    def reset(self):
        self._tag = None

    #

    @property
    def tag(self):
        if not self._tag:
            self._tag = self.random
        return self._tag

    @property
    def random(self):
        return f'{Who(self)}.tag.{randint(0, 10000000)}'


class AsyncLock(FairAsyncRLock, Logging.Mixin):

    def __str__(self):
        msg = Who(self, addr=True)
        if self._count:
            msg = f'{msg}; depth={self._count:d}, owned by: {self._owner!r}'
        return f'<{msg}>'

    async def acquire(self):
        start = time()
        result = await super().acquire()
        spent = time() - start
        if spent > 1.0:
            self.log.debug(
                f'acquired, but too late ({spent:0.4f} sec)', trace=True)
        return result


class Timeouts(dataclass.flex):

    min_quant : float = 0.25
    min_delay : float = 5.0
    max_delay : float = 300.0
    reconnect : float = 600.0


class Connection(Logging.Mixin, DumbConnection):
    _options     : ClassVar[dict] = {}
    _connections : ClassVar[dict] = {}

    @Property.Class.Parent
    def lock(cls):
        return AsyncLock()

    @classmethod
    async def make(cls, uri, **options):
        url = make_url(
                host     = uri.host,
                port     = uri.port,
                login    = uri.user,
                password = uri.password,
                virtualhost = (uri.path.strip('/')) or '/',
                **options)

        key = f'{url}:{xxh32_hexdigest(json.dumps(options, bytes=True))}'

        async with cls.lock:
            try:
                connection = cls._connections[key]
                connection_options = dict(cls._options[key])

                if options != connection_options:
                    cls.log.warning(
                        f"couldn't reinitialize connection "
                        f'{Who(connection, addr=True)} '
                        f'({url}, {connection_options=}), with another {options=}.')

            except KeyError:
                connection = cls._connections[key] = cls(url, **options)
                cls._options[key] = options.copy()

        return connection

    async def close(self):
        async with self.lock:
            if not self.is_closed:
                await super().close()
                self.log.info('closed')
            else:
                self.log.warning('already closed')

    def __init__(
        self,
        url  : HTTP.URL,
        loop : AbstractEventLoop | None = None,
        ssl_context : SSLContext | None = None,
        **kw: Any,
    ):
        self.url = url = HTTP.URL.load(url).url
        self.transport = None

        self.kwargs = self._parse_parameters(kw or dict(url.query))
        self.kwargs.setdefault('context', ssl_context)

        self.loop = loop or get_event_loop()
        self.close_callbacks = CallbackCollection(self)

        self._closed = False
        self._close_called = False
        self._active: Event = Event()

    async def _on_connection_close(self, closing: Future):
        try:  # noqa: SIM105
            e = closing.exception()
        except CancelledError as e:  # noqa: F841
            ...
        self._active.clear()
        await self.close_callbacks(e)

    async def _on_connected(self):
        self._active.set()

    async def ready(self):
        await self._active.wait()

    @property
    def is_active(self):
        return self._active.is_set()

    def __bool__(self):
        return self.is_active


class Rabbit(dataclass.auto('config')):

    class Config(dataclass.flex):
        uri     : str
        options : dict     = field(default_factory=dict)
        timeout : Timeouts = field(default_factory=Timeouts)

        prefetch  : int = 0
        consistent: bool = True

    @classmethod
    def from_url(cls, url, /, **kw):
        return cls(config=cls.Config.load(kw | {'uri': url}))

    @Property.Cached
    def url(self):
        return HTTP.URL.load(self.config.uri)

    @Property.Cached
    async def connector(self):
        return await Connection.make(self.url, **self.config.options)

    @property
    async def connection(self):
        timeout = self.config.timeout
        connector = await self.connector
        head = f'{Who(connector, addr=True)}({connector})'

        async with connector.lock:
            while not connector:
                start = time()

                await retry(
                    connector.connect,
                    traceback = False,
                    intercept = exc.RabbitExceptions,
                    maximum   = timeout.max_delay,
                )()

                if connector:
                    delta = time() - start
                    if delta < 0.1:  # noqa: PLR2004
                        self.log.info(
                            f'{head} established fast as expected')
                    elif delta < 1.0:
                        self.log.notice(
                            f'{head} established after {delta:0.2f} sec')
                    else:
                        self.log.warning(
                            f'{head} established very slow: after {delta:0.2f} sec')
                    return connector

                await sleep(timeout.min_quant)

            self.log.debug(f'{head} already connected')
        return connector

    async def __aiter__(self):

        async def cleanup(channels):
            for channel in channels:
                with suppress(Exception):
                    await channel.close()
                    self.log.verbose(f'{channel=} closed')
            return []

        channels = []

        params_channel = {'publisher_confirms': self.config.consistent}
        params_prefetch = {'prefetch_count' : 1} if self.config.prefetch else {}

        while True:
            connection = await self.connection
            try:
                async with connection.channel(**params_channel) as channel:

                    channels.append(channel)

                    while True:
                        try:
                            qos = await channel.set_qos(**params_prefetch)
                            if not isinstance(qos, cmd.Basic.QosOk):
                                self.log.info(
                                    f'{channel=} {qos=} invalid state, reconnnect')
                                break

                        except rmq.ChannelInvalidStateError:
                            self.log.info(f'{channel=} invalid state, reconnnect')
                            break

                        if channel.is_initialized and channel.is_closed:
                            self.log.info(f'{channel=} closed, reconnect')
                            break

                        yield channel

            except CancelledError as e:
                self.log.warning(f'{connection=} cancelled: {e}')

            channels = await cleanup(channels)


class Routine(dataclass.auto('config')):

    class Config(dataclass.flex):
        name      : str
        key       : str
        exchange  : str

        limit     : int | None
        encoder   : str | None

        durable   : bool | None
        active    : bool = False
        autoack   : bool = False
        exclusive : bool = False
        temporary : bool = False

        # default settings
        exchange_type       : ExchangeType | str = ExchangeType.DIRECT
        exchange_persistent : bool = True

        # lock when nobody listening tasks queue, unlock with first worker
        wait_consumers      : bool | None

        # log all slow calls
        logging_threshold   : float = 1.0

        @classmethod
        def Apply(cls, func):  # noqa: N802

            @wraps(func)
            def wrapper(self, *args, **kw):

                from kalib import halt
                if args and issubclass(Is.classOf(args[0]), Routine.Config):
                    config, args = args[0], args[1:]
                else:
                    config = self.settings

                if kw:
                    config = config.copy(**kw)
                    kw = dict(config.extra_kwargs)

                return func(self, config, *args, **kw)

            return wrapper

        @classmethod
        def FilterNone(cls, func):  # noqa: N802
            @wraps(func)
            def wrapper(*args, **kw):
                return func(*args, **{k: v for k, v in kw.items() if v is not None})
            return wrapper

        @classmethod
        def Options(cls, *fields):  # noqa: N802
            idx = set(fields)

            def container(func):
                Options = dataclass.simple(f'{Who(func)}.Options', *fields)  # noqa: N806

                @wraps(func)
                def wrapper(*args, **kw):
                    options = dict(unique(kw, include=idx))
                    options = Options.load(options)
                    return func(
                        *args, options=options,
                        **dict(unique(kw, exclude=options.as_dict)))

                return wrapper
            return container

    class Carrier(dataclass.flex):

        config   : object
        channel  : object
        exchange : object
        queue    : object

        slots : int
        limit : int | None
        tasks : int | None
        clients: int | None


        @Property.Cached
        def str(self):
            msg = f'{self.exchange}'
            if self.queue:
                msg = f'{msg}.{self.queue}'
            return f'{msg}:{self.channel}'

    class Item(dataclass):
        body: bytes | str
        mime: str

        @Property.Cached
        def charset(self):
            return Str(self.body).charset

        @Property.Cached
        def hash(self):
            return digest(self.body)

    class Solution(dataclass):
        reconnect : bool = False
        sleep     : float | int = 0.0

        def __bool__(self):
            return self.reconnect

    #

    @Property.Cached
    def settings(self):  # shortcut, can be redirected in childs
        return self.config

    @Property.Cached
    def state(self):
        return Tag.new()

    @Property.Cached
    def timeout(self):
        return self.pool.config.timeout

    @Property.Cached
    @Config.Apply
    def durable(self, config):
        if config.durable is not None:
            return (
                (DeliveryMode.NOT_PERSISTENT, DeliveryMode.PERSISTENT)
                [bool(config.durable)])

    @Property.Cached
    async def carrier_lock(self):
        connector = await self.pool.connector
        return connector.lock

    # internal methods

    @classmethod
    def from_url(cls, url, /, **kw):
        config = cls.Config.load(kw)
        rabbit = Rabbit.from_url(url, **(config.as_dict | config.extra_kwargs))
        return cls(rabbit, config=config)

    def __init__(self, pool: Rabbit, /, **kw):
        super().__init__(**kw)
        self.pool = pool

    @Config.Apply
    def dumps(self, config, data) -> Item:
        if isinstance(data, dataclass):
            data = dict(data.as_dict)

        if config.encoder:
            body = dumps(data, config.encoder)
            mime = 'application/octet-stream'
        else:
            body = json.dumps(data, bytes=True)
            mime = 'application/json'

        return self.Item.load({'body': body, 'mime': mime})

    def loads(self, msg: Message):
        return loads(msg.body) or json.loads(msg.body)

    def make(self, item, **kw):
        if not isinstance(item, self.Item):
            item = self.dumps(item)

        kw.setdefault('headers', {})
        headers = kw['headers']
        headers.setdefault('hash', item.hash)

        if kw.get('meta'):
            headers.setdefault('meta', kw.pop('meta'))

        if kw.get('reply_to'):
            headers.setdefault('reply_to', kw['reply_to'])

        if (ttl := kw.pop('ttl', None)):
            kw.setdefault('expiration', ttl)

        kw.setdefault('body', item.body)
        kw.setdefault('content_type', item.mime)
        kw.setdefault('content_encoding', item.charset)

        if self.durable is not None:
            kw.setdefault('delivery_mode', self.durable)

        return Message(timestamp=time(), **kw)

    # rabbit entities wrappers

    @Config.Apply
    @Config.FilterNone
    @Config.Options('timeout')
    @log_long_wait
    async def exchange(self, config, channel, options, **kw):  # noqa: ARG002
        exchange = config.exchange
        try:
            return await channel.declare_exchange(
                name    = exchange,
                passive = not config.active,
                type    = config.exchange_type,
                durable = config.exchange_persistent,
                timeout = options.timeout)

        except rmq.ChannelNotFoundEntity as e:
            mode = ('passive', 'active')[bool(config.active)]
            msg = f'{exchange=} {mode=} not found'
            raise exc.ExchangeNotFoundError(config, msg) from e

    @Config.Apply
    @Config.FilterNone
    @Config.Options('timeout')
    @log_long_wait
    async def queue(self, config, channel, options, **kw):  # noqa: ARG002
        queue = config.name
        try:
            return await channel.declare_queue(
                name        = queue,
                passive     = not config.active,
                durable     = config.durable or None,
                exclusive   = config.exclusive or None,
                auto_delete = config.temporary or None,
                timeout = options.timeout)

        except rmq.ChannelNotFoundEntity as e:
            mode = ('passive', 'active')[bool(config.active)]
            msg = f'{queue=} {mode=} not found'
            raise exc.QueueNotFoundError(config, msg) from e

    @Config.FilterNone
    @Config.Options('timeout', 'routing_key')
    @log_long_wait
    async def bind(self, queue, exchange, options, **kw):

        result = await queue.bind(
            exchange    = exchange,
            timeout     = options.timeout,
            routing_key = options.routing_key,
        )

        if isinstance(result, cmd.Queue.BindOk):
            return True

        kw = json.repr(kw)
        self.log.error(
            f'{exchange=} --> {queue=} ({kw=}) something went wrong')

    async def done(self, queue, text, reset=False, **kw):
        self.log.verbose(text)
        result = await queue.cancel(consumer_tag=self.state.tag, **kw)
        if reset:
            self.state.reset()
        return result

    # carrier related methods

    @Config.Apply
    @Config.Options('check_limits', 'counters', 'timeout', 'routing_key')
    async def carrier(self, config, channel, options, **kw):  # noqa: ARG002

        timeout = options.timeout or self.timeout.max_delay
        consumers, limit, slots, tasks, queue = 0, config.limit or 0, 0, 0, None

        async with await self.carrier_lock:
            exchange = await self.exchange(config, channel, timeout=timeout)
            if config.name:
                queue = await self.queue(config, channel, timeout=timeout)
                await self.bind(
                    queue, exchange,
                    timeout     = timeout,
                    routing_key = options.routing_key,
                )

        if options.check_limits or options.counters:
            if config.name is None or not queue:
                msg = f"{queue=} ({config.name=}), couldn't get queue limits"
                self.log.fatal(msg)
                raise exc.ConfigurationError(config, msg)

            declaration = queue.declaration_result
            consumers = declaration.consumer_count

            if not consumers and options.check_limits:
                msg = f'no consumers on {queue.name=}'
                self.log.warning(msg)
                if config.wait_consumers:
                    raise exc.NoActiveConsumersError(config, msg)

            tasks = declaration.message_count
            slots = max(0, limit - tasks)

            if not slots and limit > 0 and options.check_limits:
                msg = (
                    f'no free slots in {queue.name=}: awaiting {tasks=} / '
                    f'queue {limit=}, free {slots=}')
                self.log.info(msg)
                raise exc.NotAvialableQueueSlotsError(config, msg)

        return self.Carrier.load({
            'config'  : config,
            'channel' : channel,
            'exchange': exchange,
            'queue'   : queue,

            'limit'   : limit,
            'slots'   : slots,
            'tasks'   : tasks,
            'clients' : consumers,
        })

    @Property.Cached
    def _carrier_and_exceptions(self):
        return partial(
            retry,
            self.carrier,
            passthru  = True,
            traceback = False,
            limit     = self.timeout.reconnect,
            maximum   = self.timeout.max_delay), {
                TimeoutExceptions: True, (
                exc.ExchangeNotFoundError,
                exc.QueueNotFoundError,
                rmq.ChannelPreconditionFailed,
            ): False}

    @property
    def _consume_carrier(self):
        func, exceptions = self._carrier_and_exceptions
        return func(
            intercept = exceptions | {rmq.DuplicateConsumerTag: True})

    @property
    def _publish_carrier(self):
        func, exceptions = self._carrier_and_exceptions
        return func(
            intercept = exceptions | {exc.ConsumerNotReadyError: True})

    # main logic

    @Config.Apply
    def solution(self, config, exception):
        header  = f'catch ({Who(exception)}) {exception=}'
        expected, level, sleep = True, Logging.Error, self.timeout.min_delay

        kw = {}
        if issubclass(exception, TimeoutExceptions):
            level, sleep = Logging.Verbose, self.timeout.min_quant
            message = (
                f'{header}: {config.exchange}.{config.name}.{config.key} hit timeout')

        elif issubclass(exception, rmq.ChannelPreconditionFailed):
            expected = False
            message = f'{header}: configuration unexpected exception'

        elif issubclass(exception, rmq.ChannelInvalidStateError):
            level, sleep = Logging.Verbose, self.timeout.min_quant
            message = f'{header}: just refresh connection'

        elif issubclass(exception, (pam.PAMQPException, rmq.AMQPError)):
            message = f'{header}: generic rabbit unexpected exception'

        elif issubclass(exception, exc.EntityNotFoundError):
            kw['once'] = True
            expected = False
            message = f"{header}: bus entities isn't created"

        else:
            expected = False
            message = f'{header}: unexpected exception'

        trace = not expected or level is Logging.Error
        self.log.by_level(level)(message, trace=trace, stack=1, shift=-1, **kw)
        return self.Solution.load(expected, sleep)

    @Config.Apply
    @Config.Options('check_limits', 'routing_key', 'timeout')
    async def send(  # noqa: PLR0912, PLR0915, PLR0913, C901
        self, config, channel, something, /,
        message_builder=None, options=None, **kw,  # noqa: ARG002
    ):
        repeatable, result = False, []
        if message_builder and not Is.callable(message_builder):
            msg = f"({Who(message_builder)}) {message_builder=} isn't callable"
            raise TypeError(msg)

        consistent = self.pool.config.consistent
        params = {k: v for k, v in options.as_dict.items() if v is not None}
        check_limits = params.pop('check_limits', False)
        params = {
            'routing_key' : config.key,
            'timeout'     : self.timeout.max_delay,
        } | params

        if isinstance(something, Message):
            tasks = (something,)
        elif isinstance(something, list | set | tuple):
            tasks = tuple(something)
        else:
            repeatable, tasks = True, []

        while True:
            try:
                if channel.is_initialized and channel.is_closed:
                    msg = f'{Who.Is(channel)} closed'
                    raise exc.ChannelClosedError(config, msg)  # noqa: TRY301

                carrier = await self._publish_carrier(
                    config, channel, check_limits=check_limits, **params)

                if repeatable and not tasks:
                    tasks.extend(await something(carrier))

                amount = (config.limit or 0) and carrier.slots or len(tasks)
                for task in tuple(tasks[:amount]):
                    if isinstance(task, Message):
                        msg = task

                    elif message_builder:
                        msg = await message_builder(task)

                    if not isinstance(msg, Message):
                        msg = (
                            f"({carrier.str}) task isn't aio_pika.Message, "
                            f"({Who(msg)}) {msg=}")

                        await sleep(self.timeout.min_quant)
                        raise exc.ConfigurationError(carrier, msg)  # noqa: TRY301

                    start = time()
                    response = await carrier.exchange.publish(msg, **params)
                    spent = time() - start

                    maybe = '' if consistent else 'maybe '
                    msg = f'({carrier.str}) message ({len(msg.body)} bytes) {maybe}ok'

                    if consistent and (
                        isinstance(response, DeliveredMessage)
                        or not isinstance(response, cmd.Basic.Ack)
                    ):
                        msg = f"response isn't acknowledged: {response}"
                        if carrier.queue:
                            msg = (
                                f"{msg}, looks like consumer queue {config.name} "
                                f"hasn't bounded (or created) to {config.exchange=}")
                        else:
                            msg = (
                                f"{msg}, looks like {config.exchange=} isn't created "
                                f"or no queues found")

                        if config.active and isinstance(response, DeliveredMessage):
                            error = exc.PublishingMessageUnrecoverableError
                        else:
                            error = exc.PublishingMessageError

                        await sleep(self.timeout.min_quant)
                        raise error(carrier, msg)  # noqa: TRY301

                    elif not consistent:  # noqa: RET506
                        self.log.debug(
                            f'publisher confirmation disabled by {consistent=}')

                    if spent > config.logging_threshold:
                        self.log.warning(f'{msg}, but too slow, {spent:0.2f} sec')
                    else:
                        self.log.debug(msg)

                    tasks = tasks[1:]

                    if hasattr(task, 'mark_published'):
                        await task.mark_published()
                    elif hasattr(self, 'mark_published'):
                        await self.mark_published(task)

                    result.append(response)

                if not repeatable and not tasks:
                    return tuple(response)

                await sleep(self.timeout.min_quant)
                continue

            except exc.PublishingMessageError as e:
                msg = (
                    f'catch {Who(e)}, looks like broken or '
                    f'misconfigured connection: {e}')
                self.log.error(msg)  # noqa: TRY400
                break

            except exc.ConsumerNotReadyError:
                try:
                    addr = carrier.str
                except UnboundLocalError:
                    addr = config.name

                msg = (
                    f'({addr}) nobody listening or not free slots found '
                    f'for {self.timeout.reconnect:0.2f} sec, wait again')
                self.log.verbose(msg)

                await sleep(self.timeout.min_quant)
                if config.wait_consumers:
                    continue
                raise

            except Exception as e:
                if reconnect := self.solution(e):
                    await sleep(reconnect.sleep)
                    break
                await sleep(self.timeout.min_quant)
                raise

    @Config.Apply
    @Config.Options('timeout')
    async def recv(self, config, channel, callback, options, **kw):  # noqa: ARG002
        consumer, timeout = self.state, options.timeout or self.timeout.max_delay
        while True:
            if channel.is_initialized and channel.is_closed:
                msg = f'{Who.Is(channel)} closed'
                raise exc.ChannelClosedError(config, msg)

            carrier = await self._consume_carrier(config, channel, timeout=timeout)
            discard = partial(self.done, carrier.queue, timeout=timeout)

            if consumer:
                await discard(f'({carrier.str}) {consumer.tag=} restart')
            else:
                self.log.verbose(f'({carrier.str}) declare {consumer.tag=}')

            settings = {}
            if config.autoack is True:
                settings['no_ack'] = config.autoack

            try:
                async with carrier.queue.iterator(
                    consumer_tag = consumer.tag,
                    timeout      = timeout,
                    **settings,
                ) as inbox:

                    async for task in inbox:
                        result = await callback(task)
                        if result:
                            response = json.repr(result)
                            function = '' if Is.Internal(callback) else (
                                f'({Who(callback)}) ')

                            await discard(
                                f'({carrier.str}) {consumer.tag=}; got '
                                f'{function}{response=}', reset=True)
                            return result

            except TimeoutExceptions:
                msg = (
                    f'({carrier.str}) nothing received after '
                    f'{timeout:0.2f} sec, reloop and wait again')
                self.log.verbose(msg)

            except rmq.DuplicateConsumerTag as e:
                self.state.reset()
                self.log.error(  # noqa: TRY400
                    f'({carrier.str}) catch {Who(e)}, recreate consumer tag')

            except Exception as e:
                if reconnect := self.solution(e):
                    await sleep(reconnect.sleep)
                    return
                await sleep(self.timeout.min_quant)
                raise

            await sleep(self.timeout.min_quant)

    @Config.Apply
    async def perform(self, config, method, callback, *args, **kw):
        async for channel in self.pool:
            try:
                result = await method(config, channel, callback, *args, **kw)

            except exc.ChannelClosedError:
                continue

            except (exc.ExchangeNotFoundError, exc.QueueNotFoundError) as e:
                msg = f'catch {Who(e)}, mode {config.active=}'

                if not config.active:
                    self.log.warning(
                        f'{msg}, wait {self.timeout.min_delay:0.2f}s and try again')
                    await sleep(self.timeout.min_delay)
                    continue

                self.log.fatal(f'{msg}, declaration unexpected exception')
                raise

            if result is not None:
                return result

    # high level interface

    message_maker = make

    @Config.Apply
    @attach('carrier', _publish_carrier)
    async def publish(self, config, callback, /, **kw):
        kw.setdefault('check_limits', True)
        await self.perform(config, self.send, callback, **kw)

    @Config.Apply
    @attach('carrier', _consume_carrier)
    async def consume(self, config, callback, /, **kw):
        await self.perform(config, self.recv, callback, **kw)
