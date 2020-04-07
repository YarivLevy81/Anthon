import click
from .PoseParser import PoseParser
from .FeelingsParser import FeelingsParser
from .ColorImageParser import ColorImageParser
from .DepthImageParser import DepthImageParser
import uuid
import time
from . import Session
import json
import signal
from Anthon.mq_handler import MQHandler


@click.group()
def main():
    pass


@main.command()
@click.argument('parser_type')
@click.argument('path')
def parse(parser_type, path):
    parser = init_parser_type(parser_type)
    unknown_user, datetime_now = uuid.uuid4().hex, int(time.time())
    session = Session(unknown_user, datetime_now)

    result = parser.parse(path, session)
    print(f'Parsing {parser_type}..')
    return result


@main.command()
@click.argument('parser_type')
@click.argument('publisher')
def run_parser(parser_type, publisher):
    print(f'Running {parser_type} parser..')
    parser = init_parser_type(parser_type)

    mq_handler = MQHandler(publisher)
    mq_handler.init_queue(queue_name=parser_type, exchange_type='parser')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        user_id = message['user_id']
        timestamp = message['timestamp']
        snapshot_path = message['path']

        saver_message = parser.parse(snapshot_path, Session(user_id=user_id, timestamp=timestamp))
        saver_message['user_id'] = user_id
        saver_message['timestamp'] = timestamp
        saver_message['type'] = parser_type

        mq_handler.to_saver(message=saver_message)

    mq_handler.listen_to_queue(queue_name=parser_type, callback=callback)

    def signal_handler(sig, frame):
        print(f'Stopping {parser_type} parser')
        mq_handler.channel.queue_delete(queue=parser_type)
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)


def init_parser_type(parser_type: str):
    parser_type = parser_type.lower()
    if parser_type == PoseParser.parser_type:
        return PoseParser()

    if parser_type == FeelingsParser.parser_type:
        return FeelingsParser()

    if parser_type == DepthImageParser.parser_type:
        return DepthImageParser()

    if parser_type == ColorImageParser.parser_type:
        return ColorImageParser()


if __name__ == '__main__':
    main()
