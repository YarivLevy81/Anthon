import pika
from furl import furl
from enum import Enum


class MQHandler:

    def __init__(self, path):
        url = furl(path)
        if url.scheme != "rabbitmq":
            raise UnsupportedSchemeException(f'Only publisher supported is rabbitmq, ({url.scheme} is not supported)')

        # Init of broker parameters
        self.params = pika.ConnectionParameters(host=url.host, port=url.port)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()

    def init_queue(self, queue_name, exchange_type):
        # Init of parser's queue
        result = self.channel.queue_declare(queue=queue_name, exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange_type, queue=queue_name)

    def to_saver(self, message):
        self.channel.queue_declare('saver')
        self.channel.basic_publish(exchange='', routing_key='saver', body=message)

    def listen_to_queue(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def to_parsers(self, message):
        self.channel.exchange_declare(exchange='parser', exchange_type='fanout')
        self.channel.basic_publish(exchange='parser', routing_key='', body=message)


class UnsupportedSchemeException(Exception):
    pass
