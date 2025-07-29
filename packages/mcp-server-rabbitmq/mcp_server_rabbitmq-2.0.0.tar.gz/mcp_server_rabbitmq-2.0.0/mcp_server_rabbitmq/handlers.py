from typing import List

from .admin import RabbitMQAdmin
from .connection import RabbitMQConnection


def handle_enqueue(rabbitmq: RabbitMQConnection, queue: str, message: str):
    connection, channel = rabbitmq.get_channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()


def handle_fanout(rabbitmq: RabbitMQConnection, exchange: str, message: str):
    connection, channel = rabbitmq.get_channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    channel.basic_publish(exchange=exchange, routing_key="", body=message)
    connection.close()


def handle_list_queues(rabbitmq_admin: RabbitMQAdmin) -> List[str]:
    result = rabbitmq_admin.list_queues()
    return [queue["name"] for queue in result]


def handle_list_exchanges(rabbitmq_admin: RabbitMQAdmin) -> List[str]:
    result = rabbitmq_admin.list_exchanges()
    return [exchange["name"] for exchange in result]


def handle_get_queue_info(rabbitmq_admin: RabbitMQAdmin, queue: str, vhost: str = "/") -> dict:
    return rabbitmq_admin.get_queue_info(queue, vhost)


def handle_delete_queue(rabbitmq_admin: RabbitMQAdmin, queue: str, vhost: str = "/") -> None:
    rabbitmq_admin.delete_queue(queue, vhost)


def handle_purge_queue(rabbitmq_admin: RabbitMQAdmin, queue: str, vhost: str = "/") -> None:
    rabbitmq_admin.purge_queue(queue, vhost)


def handle_delete_exchange(rabbitmq_admin: RabbitMQAdmin, exchange: str, vhost: str = "/") -> None:
    rabbitmq_admin.delete_exchange(exchange, vhost)


def handle_get_exchange_info(
    rabbitmq_admin: RabbitMQAdmin, exchange: str, vhost: str = "/"
) -> dict:
    return rabbitmq_admin.get_exchange_info(exchange, vhost)
