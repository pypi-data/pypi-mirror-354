import asyncio.exceptions as aio

import aiormq.exceptions as rmq
import pamqp.exceptions as pam

from karq.retry import ExceptionsContainer, NetworkExceptions, VerboseError


class RabbitError(VerboseError):
    ...


class ConfigurationError(VerboseError):
    ...


class EntityNotFoundError(ConfigurationError):
    ...


class ExchangeNotFoundError(EntityNotFoundError):
    ...


class QueueNotFoundError(EntityNotFoundError):
    ...


class MessagesFlowControrError(VerboseError):
    ...


class ChannelClosedError(MessagesFlowControrError):
    ...


class MessagesFlowError(VerboseError):
    ...


class ConsumerNotReadyError(MessagesFlowError):
    ...


class NoActiveConsumersError(ConsumerNotReadyError):
    ...


class NotAvialableQueueSlotsError(ConsumerNotReadyError):
    ...


class ProducingFlowError(MessagesFlowError):
    ...


class PublishingMessageUnrecoverableError(MessagesFlowError):
    ...


class PublishingMessageError(MessagesFlowError):
    ...


class ProduceTasksAmountError(MessagesFlowError):
    ...


class IncorrectProducedTasksAmountError(ProduceTasksAmountError):
    ...


class IncorrectToProduceTasksAmountError(ProduceTasksAmountError):
    ...


class RabbitExceptions(ExceptionsContainer):

    Recoverable = (
        aio.CancelledError,
        pam.AMQPChannelError,
        pam.AMQPConnectionForced,
        rmq.AMQPConnectionError,
        rmq.ChannelClosed,
        rmq.ChannelInvalidStateError,
        rmq.ConnectionClosed,
        *NetworkExceptions.Recoverable)

    Expected = (
        pam.PAMQPException,
        rmq.AMQPError,
    )

    NotFound = (
        rmq.ChannelNotFoundEntity,
        EntityNotFoundError,
    )
