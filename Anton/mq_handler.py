import pika
from furl import furl
from Anton.common import UnsupportedSchemeException


PARSERS_EXCHANGE_TYPE = 'parser'
PARSERS_ROUTING_KEY = ''
SAVER_ROUTING_KEY = 'saver'
SAVER_QUEUE_NAME = SAVER_ROUTING_KEY
SAVER_EXCHANGE_KEY = ''


class MQHandler:

    def __init__(self, path):
        url = furl(path)
        if url.scheme != "rabbitmq":
            raise UnsupportedSchemeException(f'Only publisher supported is rabbitmq, ({url.scheme} is not supported)')

        # Init of broker parameters
        self.params = pika.ConnectionParameters(host=url.host, port=url.port)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=PARSERS_EXCHANGE_TYPE, exchange_type='fanout')

    def init_parser_queue(self, queue_name, exchange_type):
        # Init of parser's queue
        result = self.channel.queue_declare(queue=queue_name, exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange_type, queue=queue_name)

    def init_saver_queue(self):
        self.channel.queue_declare(SAVER_QUEUE_NAME)

    def to_saver(self, message):
        self.channel.queue_declare(SAVER_QUEUE_NAME)
        self.channel.basic_publish(exchange=SAVER_EXCHANGE_KEY, routing_key=SAVER_ROUTING_KEY, body=message)

    def listen_to_saver_queue(self, callback):
        self.listen_to_queue(queue_name=SAVER_QUEUE_NAME, callback=callback)

    def listen_to_queue(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def to_parsers(self, message):
        self.channel.exchange_declare(exchange=PARSERS_EXCHANGE_TYPE, exchange_type='fanout')
        self.channel.basic_publish(exchange=PARSERS_EXCHANGE_TYPE, routing_key=PARSERS_ROUTING_KEY, body=message)



