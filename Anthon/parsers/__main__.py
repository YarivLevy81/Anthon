import click
from .PoseParser import PoseParser
from .FeelingsParser import FeelingsParser
from .ColorImageParser import ColorImageParser
from .DepthImageParser import DepthImageParser
from . import Session
import json
import signal
import Anthon.mq_handler as MQHandler
import Anthon.common as Common


@click.group()
def main():
    pass


@main.command()
@click.argument('parser_type')
@click.argument('path')
def parse(parser_type, path):
    parser = init_parser_type(parser_type)

    file = open(path, 'rb')
    data = file.read()
    json_data = json.loads(data)

    snapshot_path = json_data[Common.SNAPSHOT_PATH_FIELD]
    user_id       = json_data[Common.USER_ID_FIELD]
    snapshot_id   = json_data[Common.SNAPSHOT_ID_FIELD]

    session = Session(user_id=user_id, snapshot_id=snapshot_id)
    result = parser.parse(snapshot_path, session)
    result.update(json_data)

    print(json.dumps(result))
    return json.dumps(result)


@main.command('run-parser')
@click.argument('parser_type')
@click.argument('publisher')
def run_parser_cli(parser_type, publisher):
    run_parser(parser_type=parser_type, publisher=publisher)


def run_parser(parser_type, publisher):
    print(f'Running {parser_type} parser..')
    parser = init_parser_type(parser_type)

    mq_handler = MQHandler.MQHandler(publisher)
    mq_handler.init_parser_queue(queue_name=parser_type, exchange_type=MQHandler.PARSERS_EXCHANGE_TYPE)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        user_id = message[Common.USER_ID_FIELD]
        snapshot_id = message[Common.SNAPSHOT_ID_FIELD]
        snapshot_path = message[Common.SNAPSHOT_PATH_FIELD]

        saver_message = parser.parse(snapshot_path, Session(user_id=user_id, snapshot_id=snapshot_id))
        saver_message.update(message)
        saver_message[Common.TYPE_FIELD] = parser_type
        saver_message = json.dumps(saver_message)

        mq_handler.to_saver(message=saver_message)

    # This line will block until SIGINT\SIGTERM\SIGKILL is received
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
