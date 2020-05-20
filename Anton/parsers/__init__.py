from Anton.parsers.Session import Session
from Anton.parsers.PoseParser import PoseParser
from Anton.parsers.FeelingsParser import FeelingsParser
from Anton.parsers.ColorImageParser import ColorImageParser
from Anton.parsers.DepthImageParser import DepthImageParser
import json
import signal
from Anton.mq_handler import *
from Anton.common import *
import pathlib
from Anton.common import bcolors

ERRNO_UNKNOWN_PARSER_TYPE = -2
ERRNO_FILE_NOT_EXIST = - 3
ERRNO_FILE_FORMAT = -4
ERRNO_UNSUPPORTED_SCHEME = -5


def parse(parser_type, path):
    parser = init_parser_type(parser_type)
    if parser is None:
        print(f'{bcolors.FAIL}ERROR: parser {parser_type} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNKNOWN_PARSER_TYPE)

    if not pathlib.Path(path).exists() or not pathlib.Path(path).is_file():
        print(f'{bcolors.FAIL}ERROR: No such file {path} {bcolors.ENDC}')
        exit(ERRNO_FILE_NOT_EXIST)

    try:
        file = open(path, 'rb')
        data = file.read()
        json_data = json.loads(data)

        snapshot_path = json_data[SNAPSHOT_PATH_FIELD]
        user_id       = json_data[USER_ID_FIELD]
        snapshot_id   = json_data[SNAPSHOT_ID_FIELD]

        session = Session(user_id=user_id, snapshot_id=snapshot_id)
        result = parser.parse(snapshot_path, session)
        result.update(json_data)

        print(json.dumps(result))
        return json.dumps(result)

    except (KeyError, json.decoder.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
        print(f'{bcolors.FAIL}ERROR: File {path} is not formatted (see docs){bcolors.ENDC}')
        exit(ERRNO_FILE_FORMAT)


def run_parser(parser_type, publisher):
    print(f'Running {parser_type} parser..')
    parser = init_parser_type(parser_type)
    if parser is None:
        print(f'{bcolors.FAIL}ERROR: parser {parser_type} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNKNOWN_PARSER_TYPE)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        user_id = message[USER_ID_FIELD]
        snapshot_id = message[SNAPSHOT_ID_FIELD]
        snapshot_path = message[SNAPSHOT_PATH_FIELD]

        saver_message = parser.parse(snapshot_path, Session(user_id=user_id, snapshot_id=snapshot_id))
        saver_message.update(message)
        saver_message[TYPE_FIELD] = parser_type
        saver_message = json.dumps(saver_message)

        mq_handler.to_saver(message=saver_message)

    def signal_handler(sig, frame):
        print(f'Stopping {parser_type} parser')
        mq_handler.channel.queue_delete(queue=parser_type)
        exit(0)

    try:
        mq_handler = MQHandler(publisher)
        mq_handler.init_parser_queue(queue_name=parser_type, exchange_type=PARSERS_EXCHANGE_TYPE)
        # This line will block until SIGINT\SIGTERM\SIGKILL is received
        mq_handler.listen_to_queue(queue_name=parser_type, callback=callback)
        signal.signal(signal.SIGINT, signal_handler)
    except UnsupportedSchemeException as e:
        print(f'{bcolors.FAIL}ERROR: Publisher {e.scheme} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNSUPPORTED_SCHEME)


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

    return None


