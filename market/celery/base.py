from celery import signature

import pika
import ujson
import logging
import traceback
from celery import Task

from market.utility import get_or_none, Singleton

logger = logging.getLogger('celery')


class MarketCelery(Task):
    autoretry_for = (Exception,)
    default_retry_delay = 2
    soft_time_limit = None
    needs_token = False
    max_retries = 2
    time_limit = None
    acks_late = True

    def __call__(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user_id = kwargs.get('user_id')
        self.user = None

        if user_id:
            self.user = get_or_none(User, user_id)

        return super().__call__(*args, **kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if self.request.retries == 0:
            error_detail = ujson.dumps(dict(
                exc=exc.__doc__,
                task_id=task_id,
                stackTrace=traceback.format_exc(),
            ))
            logger.error(error_detail)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error_detail = ujson.dumps(dict(
            exc=exc.__doc__,
            task_id=task_id,
            stackTrace=traceback.format_exc(),
        ))
        logger.error(error_detail)

        try:
            backup_task = CeleryBackupMessage(
                args=ujson.dumps(args),
                kwargs=ujson.dumps(kwargs),
                task_name=self.name,
                fail_reason=error_detail,
                task_id=task_id,
            )
            CeleryRequeue().sender(backup_task.to_json())
        except Exception as exc_:  # pragma: no cover
            logger.critical(ujson.dumps(dict(
                message=exc_.__doc__,
                stackTrace=traceback.format_exc(),
                taskId=task_id,
            )))


class CeleryBackupMessage:

    def __init__(
            self,
            task_name: str,
            args: tuple,
            kwargs: dict,
            fail_reason: str,
            task_id: str
    ):
        self.task_name = task_name
        self.args = args
        self.kwargs = kwargs
        self.fail_reason = fail_reason
        self.task_id = task_id

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary containing relevant
        attributes.

        Returns:
            dict: A dictionary containing keys and values representing the
                object's attributes including 'task, _name', 'args', 'kwargs',
                'fail_reason', and 'task_id'.
        """
        return dict(
            task_name=self.task_name,
            args=self.args,
            kwargs=self.kwargs,
            fail_reason=self.fail_reason,
            task_id=self.task_id,
        )

    def to_json(self) -> str:
        """Converts the object to a JSON formatted string.

        Returns:
            str: JSON string representation of the object.
        """
        return ujson.dumps(
            self.to_dict(),
            escape_forward_slashes=False,
            indent=4,
        )

    @classmethod
    def to_instance(cls, json_message: str) -> object:
        """Convert a JSON message into an instance of the class.

        Args:
            json_message (str): A JSON formatted string representing the class
                attributes.

        Returns:
            object: An instance of the cls constructed from the JSON message.
        """
        return cls(**ujson.loads(json_message))


class CeleryRequeue(metaclass=Singleton):

    def __init__(self):
        self.host = 'localhost'
        self.exchange_name = 'market_celery_requeue'
        self.exchange_type = 'direct'
        self.queue_name = 'market_requeue'
        self.routing_key = 'market_requeue'
        self.heartbeat = 2
        self.max_priority = 10
        self._create_connection()

    def _create_connection(self):
        parameters = pika.ConnectionParameters(
            host=self.host,
            heartbeat=self.heartbeat,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
        self.queue = self.channel.queue_declare(queue=self.queue_name, durable=True, arguments={'x-max-priority': self.max_priority},)
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.routing_key)

    def _sender(self, message: str, priority: int) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
            properties=pika.BasicProperties(priority=priority),
        )
        logger.info('Message published in requeue')

    def sender(self, message: str, priority: int = None):
        try:
            try:

                self._sender(message, priority)

            except Exception as exp:  # pragma: no cover
                error_message = dict(
                    stackTrace=traceback.format_exc(),
                    message=exp.__doc__,
                )
                logger.error(error_message)

                self._create_connection()
                self._sender(message, priority)

        except Exception as exp:
            error_message = dict(
                stackTrace=traceback.format_exc(),
                message=exp.__doc__,
            )
            logger.error(error_message)
            raise exp

    def callback(self, ch, method, properties, body):
        try:
            message = CeleryBackupMessage.to_instance(body.decode())
            signature(
                message.task_name,
                args=ujson.loads(message.args),
                kwargs=ujson.loads(message.kwargs),
            ).delay()
            logger.info('Create task on call back')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exp:
            logger.critical(exp, exc_info=True)
            raise exp

    def requeue(self):
        error_message_count = self.queue.method.message_count
        if error_message_count == 0:
            # Cancel the consumer and  Close the channel and the connection
            self.channel.cancel()
            self.channel.close()
            self.connection.close()
            logger.info("Requeue done successfully")
            return

        for method, properties, body  in self.channel.consume(self.queue_name):
            self.callback(self.channel, method, properties, body)

            if method.delivery_tag == error_message_count:
                break

        # Cancel the consumer and  Close the channel and the connection
        self.channel.cancel()
        self.channel.close()
        self.connection.close()
        logger.info("Requeue done successfully")

