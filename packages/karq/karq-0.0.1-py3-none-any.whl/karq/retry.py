import asyncio  # noqa: I001
import builtins
from abc import ABC
from collections import defaultdict, deque
from collections.abc import Iterable
from functools import partial, reduce, wraps
from itertools import combinations
from logging import Logger
from math import exp
from operator import or_
from random import uniform
from time import time
from typing import Any, ClassVar

from kalib import Is, Logging, Property, Who, exception, sort, unique, dataclass


def incremental_delay(limit=None, deviation=None, function=exp):
    def wrapper(attempt, *args, **kw):
        result = function(attempt, *args, **kw)

        if deviation:
            bias = uniform(1.0 - deviation, 1.0 + deviation)  # noqa: S311
            result = uniform(result * bias, result / bias)  # ~5.54..9.85  # noqa: S311
        return float(limit if limit and result >= limit else result)
    return wrapper


def to_tuple(x):
    return tuple(x or ()) if Is.iterable(x) else (x,)


def make_properties(klass):

    def make_wrapper(name):
        def wrapper(cls):
            return to_tuple(getattr(cls, name))
        return wrapper

    for name in klass.attrs:
        func = name.lower()
        wrapper = make_wrapper(name)
        wrapper.__name__ = func
        wrapper.__qualname__ = f'{Who(klass, full=False)}.{func}'

        if hasattr(klass, func):
            msg = f'property {wrapper.__qualname__} already exists'
            raise ValueError(msg)
        setattr(klass, func, Property.Class(wrapper))

    return klass


def positive_numeric(func):
    @wraps(func)
    def wrapped(self, *args, **kw):
        result = func(self, *args, **kw)
        if not isinstance(result, float | int) or result < 0:
            msg = (
                f'{Who(func)} must be positive numeric, '
                f'not ({Who(result)}) {result=}')
            raise ValueError(msg)
        return result
    return wrapped


class Exceptions(dataclass):

    recover : list[Exception] = ()
    expect  : list[Exception] = ()
    suppress: list[Exception] = ()


@make_properties
class ExceptionsContainer(Logging.Mixin):

    attrs = ('Expected', 'Recoverable')

    @Property.Class.Cached
    def order(cls):
        result = {}
        attrs = set(cls.attrs)
        keys = tuple(cls.__dict__)

        if attrs & set(keys):
            for key in keys:
                if key in attrs:
                    exceptions = getattr(cls, key.lower())
                    if exceptions:
                        result[exceptions] = key == 'Recoverable'

        return dict(result)


class VerboseError(ABC, Exception):
    def __init__(self, *args):
        if len(args) == 2:  # noqa: PLR2004
            item, message = args
            super().__init__(f'({Who(item)}) {item!r}: {message}')

        elif len(args) == 1:
            super().__init__(args[0])

        else:
            msg = (
                f'{Who(self)} can use 1 or 2 arguments, '
                f'not {len(args)}: {args!r}')
            raise ValueError(msg)


class RetryError(Exception):
    ...


class TaskTimedoutError(RetryError):
    ...


class WrappedTaskTimeoutError(RetryError):
    ...


TimeoutExceptions = (
    TimeoutError,
    asyncio.TimeoutError,
    builtins.TimeoutError,
    TaskTimedoutError)


class NetworkExceptions(ExceptionsContainer):
    Recoverable = (
        ConnectionError,
        ConnectionRefusedError,
        *TimeoutExceptions)


class BuiltinExceptions(ExceptionsContainer):
    Expected = (
        AttributeError, KeyError, ValueError,
        AssertionError, BufferError, EOFError, ImportError, LookupError,
        MemoryError, NameError, ReferenceError, StopAsyncIteration,
        StopIteration, SyntaxError, SystemError, TypeError, ValueError)



class Retry(dataclass.auto('config')):
    ContainerMixin = ExceptionsContainer
    _exceptions_groups_cache: ClassVar[dict] = {}

    class Config(dataclass.flex):

        # global limits
        count : int = 0  # max tries count
        limit : bool | int | float = 0.0  # relative +sec or absolute unix timestamp

        # per task limits
        timeout : float = 0.0  # max function call execution time
        minimum : float = 0.0  # min sleep time between retries
        maximum : float = 0.0  # max sleep time

        # basic logging configuration
        passthru  : bool = False # passthru exception when deadline reached
        traceback : bool | None = None  # show traceback always or only first time

        # exceptions configuration
        logging   : dict[Exception, Any] | bool | None = False
        intercept : (
            Exception |
            Iterable[Exception] |
            dict[Exception, bool] |
            ExceptionsContainer |
            Any)

    @Property.Cached
    def logger(self):
        return self._logger or Logging.get(self)

    def __init__(self, func, logger: Logger | None = None, /, **config):
        if logger is not None and not Is.subclass(logger, Logger):
            msg = (
                f'logger must be instance of {Who(Logger)}, '
                f'not ({Who(logger)}) {logger=}')
            raise TypeError(msg)

        # static data
        self._func = func
        self._logger = logger

        # internal variables
        self._start = None
        self._counter = 0
        self._history = []
        self._timeouts = deque(maxlen=2 ** 10)

        super().__init__(config=config)

    # static properties

    @Property.Cached
    def function(self):
        return self._func

    @Property.Cached
    @positive_numeric
    def timeout(self):
        timeout = self.config.timeout
        return (
            float(timeout)
            if isinstance(timeout, float | int) and timeout > 0 else 0.0)

    @Property.Cached
    def logging(self):
        logging = self.config.logging

        if logging is None or isinstance(logging, bool):
            return {Exception: logging}

        if not isinstance(logging, dict):
            msg = f'({Who(logging)}) {logging=} must me dict or bool'
            raise TypeError(msg)

        return self.solutions(logging)

    @property
    def show_traceback(self):
        traceback = self.config.traceback
        return traceback or (traceback is None and self.counter == 1)

    @Property.Cached
    @positive_numeric
    def minimum(self):
        return self.config.minimum

    @Property.Cached
    @positive_numeric
    def maximum(self):
        return self.config.maximum

    @Property.Cached
    @positive_numeric
    def count(self):
        return self.config.count

    @property
    @positive_numeric
    def deadline(self):
        limit = self.config.limit

        if limit is True:
            if not self.maximum:
                self.log.warning(
                    f'{limit=}, but {self.maximum=}, disable deadlining')
            limit = self.maximum

        elif not isinstance(limit, float | int):
            return limit

        if not limit:
            return 0.0

        if limit <= 365 * 10:
            limit += time()

        return limit

    @Property.Cached
    def sleep_time(self):
        return incremental_delay(self.maximum)

    # active properties

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        if not isinstance(counter, int):
            msg = f'({Who(counter)}) {counter=} must me positive integer'
            raise TypeError(msg)
        counter = int(counter)
        self._counter = counter
        return counter

    @property
    def exception(self):
        try:
            return self._history[-1]

        except IndexError:
            msg = f'{Who(self)}.exception is never set'
            raise ValueError(msg)  # noqa: B904, TRY200

    @exception.setter
    def exception(self, e):
        if not Is.subclass(e, Exception):
            msg = f'({Who(e)}) {e=} must be inherited from Exception'
            raise TypeError(msg)

        self._history.append(e)
        return self._history[-1]

    @property
    def start(self):
        start = self._start
        if start is None:
            msg = f'({Who(start)}) {start=} is never set'
            raise ValueError(msg)
        return start

    @start.setter
    def start(self, start):
        if not isinstance(start, float | int):
            msg = f'({Who(start)}) {start=} must me positive float'
            raise TypeError(msg)
        start = float(start)

        self._start = start
        return start

    @property
    def average(self):
        if not self._timeouts:
            msg = f'{Who(self)}.average never set'
            raise ValueError(msg)
        return sum(self._timeouts) / len(self._timeouts)

    @average.setter
    def average(self, start):
        if not isinstance(start, float | int):
            msg = f'({Who(start)}) {start=} must me positive float'
            raise TypeError(msg)

        value = time() - float(start)
        self._timeouts.append(value)
        return value

    # exceptions order configuration methods

    def validate(self, order):
        seen = set()
        shadows = []
        for no, stage in enumerate(order):
            if not no:
                seen.update(stage)
                continue

            mode = ('expected', 'recoverable')[order[stage]]
            for e in stage:
                if Is.subclass(e, to_tuple(seen)):
                    for num, ee in enumerate(order):
                        if Is.subclass(e, to_tuple(ee)):
                            shadows.append(
                                f'{mode} {Who(e)} at stage '
                                f'{no} shadowed by stage {num}')
                            break
            seen.update(stage)

        if shadows:
            self.log.trace(
                f'some exceptions never intercept: {"; ".join(shadows)}')

        return dict(order)

    def flattened_solutions(self, order):  # noqa: PLR0912

        def by_depth(x):
            return str(Who(x).count('.')) + Who(x)

        last = None
        result = []
        for stage, solution in order.items():
            if last is None:
                result.append( [solution, *stage] )
                last = solution
                continue

            if solution is not last:
                result.append([solution])
                last = solution

            result[-1].extend(stage)

        union_stages = {}
        for solution, *stage in result:
            union_stages[tuple(stage)] = solution

        ordered_stages = []
        for stage in reversed(union_stages):
            try:
                ordered_stages.append(self._exceptions_groups_cache[stage])

            except KeyError:
                classes_to_remove = set()
                parent_to_childs = defaultdict(set)
                childs_to_parent = defaultdict(set)

                for foo, bar in combinations(stage, 2):
                    if foo is bar:
                        continue

                    if Is.subclass(foo, bar):
                        parent_to_childs[bar].add(foo)
                        childs_to_parent[foo].add(bar)

                    elif Is.subclass(bar, foo):
                        parent_to_childs[foo].add(bar)
                        childs_to_parent[bar].add(foo)

                parent_to_childs = dict(parent_to_childs)
                childs_to_parent = dict(childs_to_parent)

                if parent_to_childs:
                    duplicated = set(unique(reduce(or_,
                        ((parent_to_childs.get(e, set()) | {e})
                            for e in childs_to_parent))))

                    for e in duplicated:
                        classes_to_remove.add(e)
                        if e in parent_to_childs:
                            classes_to_remove.update(parent_to_childs[e])

                    pivots = defaultdict(set)
                    for e in classes_to_remove:
                        for pivot in childs_to_parent[e] - classes_to_remove:
                            pivots[pivot].add(e)

                    result = []
                    for e in sort(pivots, key=by_depth):
                        result.append(
                            f'({", ".join(sort(map(Who, pivots[e])))}) '
                            f'-> {Who(e)}')

                    self.log.debug(
                        f'remove duplicated: {"; ".join(result)}')

                reordered = tuple(sorted(
                    unique(stage, exclude=classes_to_remove),
                    key=lambda x: len(Is.classOf(x).__mro__), reverse=True))

                ordered_stages.append(reordered)
                self._exceptions_groups_cache[stage] = reordered

        return self.validate(
            dict(zip(
                reversed(ordered_stages),
                union_stages.values(), strict=True)))

    def solutions(self, something):
        invalid_message = (
            f'intercepted exceptions order can be Exception, '
            f'dict[Exception, bool], Iter[Exception], '
            f'or {Who.Is(ExceptionsContainer)} '
            f'not {Who.Is(something)}; '
            f'check closest {Who(self)} invocation')

        def make_tuple(x):
            if Is.subclass(x, Exception):
                return {(x,): True}

            elif x is BaseException:
                msg = f'never try to catch BaseException: {Who.Is(x)}'
                raise ValueError(msg)

            elif Is.subclass(x, ExceptionsContainer):
                return make_tuple(x.order)

            elif Is.subclass(x, asyncio.exceptions.CancelledError):
                return {(x,): True}

            result = {}

            def propagate_order(result, order):
                result = dict(result)
                for k, v in order.items():
                    if k not in result:
                        result[to_tuple(k)] = v
                    else:
                        pass
                return dict(result)

            if isinstance(x, dict):
                return propagate_order(result, x)

            elif isinstance(x, list | set | tuple):
                for i in x:
                    result = propagate_order(result, make_tuple(i))
                return result

            raise TypeError(invalid_message)

        if something is all:
            something = [{Exception: True}]

        elif something is any:
            something = [{BuiltinExceptions.Expected: False, Exception: True}]

        elif not something:
            raise ValueError(invalid_message)

        order = make_tuple(something)
        if not order:
            raise ValueError(invalid_message)

        exceptions = self.flattened_solutions(order)
        if (
            len(exceptions) == 1 and
            not (key := next(iter(exceptions))) and
            isinstance(key, tuple)
        ):
            self.log.trace(
                f"empty recoverable {exceptions=} order, let's intercept "
                f'any exception! (but rewrite with intercept=any kwarg)')
            exceptions = {(Exception,): True}

        return dict(exceptions)

    def get_exception_value_from_order(self, exceptions, exception, /, **kw):
        for stage, value in exceptions.items():
            if Is.subclass(exception, stage):
                return value
        try:
            return kw['default']
        except KeyError:
            msg = f'{exception=} not in {exceptions=}'
            raise KeyError(msg)  # noqa: B904, TRY200

    def intercept(self, exception, message, full=False, level=None, **kw):
        if full:
            message = f'{Who(exception)}: {exception=}; {message}'

        level = level or self.get_exception_value_from_order(
            self.logging, exception, default=Logging.Verbose)

        kw.setdefault('trace', self.show_traceback)
        self.log.by_level(level)(message, **kw)

    def passthru(self, message):
        exception = self.exception

        message = f'{message}, raise ({Who(exception)})'
        if not Is.Class(exception):
            message = f'{message} {exception=}'
        self.intercept(exception, message)


        if (
            not self.config.passthru or
            Is.classOf(exception) is WrappedTaskTimeoutError
        ):
            raise TaskTimedoutError from exception
        raise exception

    # prepared exceptions properties

    @Property.Cached
    def expected(self):
        exceptions = []
        for e, recoverable in self.exceptions.items():
            if recoverable:
                exceptions.extend(e)
        return next(iter(self.solutions(exceptions)))

    @Property.Cached
    def exceptions(self):
        return self.solutions(self.config.intercept)

    # main methods

    def solution(self, message, exceptions, deadline, start):
        now = time()

        self.average = start
        exception = self.exception

        if Is.subclass(exception, WrappedTaskTimeoutError):
            can_recover = True
        else:
            try:
                can_recover = self.get_exception_value_from_order(exceptions, exception)
            except KeyError:
                return

        self.counter += 1
        count = self.count

        message = (
            f'{self.counter}/{count}. ' if count else f'{self.counter}. '
            f'after {now - start:0.3f}/{now - self.start:0.3f} sec, {message}')

        if count and self.counter >= count:
            message = f'{message}, maximum {count=} reached'
            self.passthru(message)

        if not can_recover:
            self.intercept(
                exception, f'{message} got expected {Who(exception)}, raise')
            raise exception

        wait = self.sleep_to
        message = f'{message} got {Who(exception)}'

        if deadline:
            if now > deadline:
                overdue = now - deadline
                message = (
                    f'{message}, deadline +{(now - self.start):0.2f} '
                    f'sec reached')
                if overdue >= 0.1:  # noqa: PLR2004
                    message = '{message}, overdue {overdue:0.2f} sec'
                self.passthru(message)

            plan = deadline - now - self.average
            if plan < 0:
                message = (
                    f'{message}, deadline {deadline:0.2f} '
                    f'(average {self.average:0.2f}) after '
                    f'{(now - deadline):0.2f} sec, can be reached')
                self.passthru(message)

            if plan < wait:
                message = (
                    f'{message}, retry wait {wait:0.2f} > deadline '
                    f'{(deadline - now):0.2f} - {self.average:0.2f}, '
                    f'shrink sleep time to {plan:0.2f} sec')
                wait = plan

        message = f'{message}, sleep {wait:0.2f} sec'
        if deadline and (delta := (deadline - time())) and delta < wait:
            message = f'{message}, last chance after {delta:0.2f} sec'

        self.intercept(exception, message)
        return wait

    @property
    def sleep_to(self):
        return max(self.minimum, self.sleep_time(self.counter))

    @classmethod
    def make(cls, *args, **kw):
        self = cls(*args, **kw)

        def override_exception(data, key, value):
            if (order := data.pop(key, None)):
                if Is.subclass(order, Exception):
                    return {(order,): value}

                if not isinstance(order, list | set | tuple):
                    msg = (
                        f'{Who(order)} {order=} must be '
                        f'Exception, tuple or list')
                    raise TypeError(msg)

                return {to_tuple(order): value}

            return {}

        @wraps(self.function)
        async def retry(*args, **kw):  # noqa: PLR0912
            self.start = time()

            order = (
                override_exception(kw, 'recover', False),  # noqa: FBT003
                override_exception(kw, 'expect', True),  # noqa: FBT003
                self.exceptions)

            kw = {**self.config.extra_kwargs, **kw}
            header = f'{Who(self.function)}({args=}, {kw=})'
            deadline = self.deadline

            exceptions = {}
            for stage in order:
                for key, value in stage.items():
                    if key in exceptions:
                        msg = f'{header} {key=} already defined, override with {value=}'
                        self.log.warning(msg)
                    exceptions[key] = value
            exceptions = self.solutions(exceptions)

            order = '; '.join(
                f'{("throw expected", "handle recoverable")[recoverable]} '
                f'[{", ".join(map(Who, stage))}]'
                    for stage, recoverable in exceptions.items())
            self.log.verbose(f'{header} {order}', once=True)

            solution = partial(self.solution, header, exceptions, deadline)
            while True:
                task = self.function(*args, **kw)
                coro = asyncio.create_task(task)

                start = time()
                try:
                    if self.timeout:
                        return await asyncio.wait_for(coro, timeout=self.timeout)
                    else:
                        return await coro

                except Exception as exception:

                    if Is.substance(exception, asyncio.TimeoutError):
                        state = coro._state  # noqa: SLF001

                        if state == 'CANCELLED':
                            exception, timeout = WrappedTaskTimeoutError, self.timeout
                            self.intercept(
                                exception, f'{header} catch wrapper '
                                f'{timeout=}, {Who.Is(state)=}')

                        elif state == 'FINISHED':
                            self.intercept(
                                exception, f'{header} throw '
                                f'{exception=}, {Who.Is(state)=}')
                        else:
                            msg = f'unexpected task {task=} ({coro=}) {state=}'
                            raise ValueError(msg)  # noqa: B904, TRY200

                    self.exception = exception
                    sleep = solution(start)

                    if sleep is not None:
                        await asyncio.sleep(sleep)
                        continue

                    self.intercept(
                        exception, f'{header} got unhandled '
                        f'{Who(exception)}, after {self.counter} attempt',
                        level=Logging.Error)
                    raise

        retry.expectations = self.expected
        retry.cancelled = TaskTimedoutError
        return retry


def format_exception(e):
    return exception(e).as_dict | {
        'class'  : Who(e),
        'source' : Who.File(e)}


retry = Retry.make
