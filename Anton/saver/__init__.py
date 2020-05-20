import sys
import os
from Anton.mq_handler import MQHandler
from Anton.saver.MongoHandler import MongoHandler, ResultEntry, UserEntry
import json
from Anton.common import *
import pathlib
sys.path.append(os.path.join(os.path.dirname(__file__)))


ERRNO_FILE_NOT_EXIST = -2
ERRNO_FILE_FORMAT = -3
ERRNO_UNSUPPORTED_SCHEME = -4


def save(database, topic, path):

    try:
        mongo_handler = MongoHandler(path=database)

        if not pathlib.Path(path).exists() or not pathlib.Path(path).is_file():
            print(f'{bcolors.FAIL}ERROR: No such file {path} {bcolors.ENDC}')
            exit(ERRNO_FILE_NOT_EXIST)

        json_message = None
        if type(path) == str:
            file = open(path, 'rb')
            json_message = json.loads(file.read())
        elif type(path) == dict:
            json_message = path

        if topic not in json_message:
            raise KeyError("Result type of the data doesn't seem to match topic")

        save_snapshot(db_handler=mongo_handler, json_message=json_message, topic=topic)

    except UnsupportedSchemeException as e:
        print(f'{bcolors.FAIL}ERROR: Database {e.scheme} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNSUPPORTED_SCHEME)
    except (KeyError, json.decoder.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
        print(f'{bcolors.FAIL}ERROR: File {path} is not formatted (see docs){bcolors.ENDC}')
        exit(ERRNO_FILE_FORMAT)


def save_snapshot(db_handler, json_message, topic):
    user_id = json_message[USER_ID_FIELD]
    username = json_message[USERNAME_FIELD]
    birthdate = json_message[BIRTHDATE_FIELD]
    gender = json_message[GENDER_FIELD]

    data = json_message[topic]
    timestamp = json_message[TIMESTAMP_FIELD]
    snapshot_id = json_message[SNAPSHOT_ID_FIELD]
    snapshot_path = json_message[SNAPSHOT_PATH_FIELD]

    user_entry = UserEntry(user_id=user_id, username=username, birthdate=birthdate, gender=gender)
    result_entry = ResultEntry(user_id=user_id, snapshot_id=snapshot_id, snapshot_path=snapshot_path,
                               timestamp=timestamp, result_type=topic, result_data=data)

    db_handler.save_user(user_entry=user_entry)
    db_handler.save_snapshot_result(result_entry=result_entry)


def run_saver(database, publisher):

    try:
        mongo_handler = MongoHandler(path=database)
        mq_handler = MQHandler(path=publisher)

        mq_handler.init_saver_queue()

        def callback(ch, method, properties, body):
            json_message = json.loads(body)
            parser_type = json_message[TYPE_FIELD]
            save_snapshot(db_handler=mongo_handler, json_message=json_message, topic=parser_type)

        mq_handler.listen_to_saver_queue(callback=callback)
    except UnsupportedSchemeException as e:
        print(f'{bcolors.FAIL}ERROR: Database {e.scheme} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNSUPPORTED_SCHEME)



