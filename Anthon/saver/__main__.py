import click
from .MongoHandler import MongoHandler, MONGO_DEFAULT_PATH
from Anthon.mq_handler import MQHandler, UnsupportedSchemeException
import json
import Anthon.common as Common
from Anthon.saver import ResultEntry, UserEntry


@click.group()
def main():
    pass


@main.command()
@click.argument('database')
@click.argument('publisher')
def run_saver(database, publisher):

    # TODO: Handle exceptions
    mongo_handler = MongoHandler(path=database)
    mq_handler = MQHandler(path=publisher)

    mq_handler.init_saver_queue()

    def callback(ch, method, properties, body):
        json_message = json.loads(body)
        parser_type = json_message[Common.TYPE_FIELD]
        save_snapshot(db_handler=mongo_handler, json_message=json_message, topic=parser_type)

    mq_handler.listen_to_saver_queue(callback=callback)


@main.command('save')
@click.option("--database", "-d", default=MONGO_DEFAULT_PATH)
@click.argument('topic')
@click.argument('path')
def save_cli(database, topic, path):
    save(database=database, topic=topic, path=path)


def save(database, topic, path):
    print(database)
    # TODO: Handle exceptions
    mongo_handler = MongoHandler(path=database)
    print(type(path))

    json_message = None
    if type(path) == str:
        file = open(path, 'rb')
        json_message = json.loads(file.read())
    elif type(path) == dict:
        json_message = path

    if topic not in json_message:
        raise Warning("Result type of the data doesn't seem to match topic")

    save_snapshot(db_handler=mongo_handler, json_message=json_message, topic=topic)


def save_snapshot(db_handler, json_message, topic):
    user_id = json_message[Common.USER_ID_FIELD]
    username = json_message[Common.USERNAME_FIELD]
    birthdate = json_message[Common.BIRTHDATE_FIELD]
    gender = json_message[Common.GENDER_FIELD]

    data = json_message[topic]
    timestamp = json_message[Common.TIMESTAMP_FIELD]
    snapshot_id = json_message[Common.SNAPSHOT_ID_FIELD]
    snapshot_path = json_message[Common.SNAPSHOT_PATH_FIELD]

    user_entry = UserEntry(user_id=user_id, username=username, birthdate=birthdate, gender=gender)
    result_entry = ResultEntry(user_id=user_id, snapshot_id=snapshot_id, snapshot_path=snapshot_path,
                               timestamp=timestamp, result_type=topic, result_data=data)

    db_handler.save_user(user_entry=user_entry)
    db_handler.save_snapshot_result(result_entry=result_entry)


if __name__ == '__main__':
    main()
