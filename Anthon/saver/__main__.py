import click
from furl import furl
from .MongoHandler import MongoHandler, MONGO_DEFAULT_PATH
from Anthon.mq_handler import MQHandler, UnsupportedSchemeException
import json
import Anthon.common as Common
from Anthon.saver import ResultEntry, UserEntry


@click.group()
def main():
    pass


@main.command()
@click.option("--database", "-d", default=MONGO_DEFAULT_PATH)
@click.argument('topic')
@click.argument('path')
def save(database, topic, path):
    print(database)
    url = furl(database)
    if url.scheme != "mongodb":
        raise UnsupportedSchemeException(f'Only database supported is mongodb, ({url.scheme} is not supported)')
    mongo_handler = MongoHandler(host=url.host, port=url.port)

    file = open(path, 'rb')
    json_message = json.loads(file.read())

    if topic not in json_message:
        raise Warning("Result type of the data doesn't seem to match topic")

    user_id       = json_message[Common.USER_ID_FIELD]
    username      = json_message[Common.USERNAME_FIELD]
    birthdate     = json_message[Common.BIRTHDATE_FIELD]
    gender        = json_message[Common.GENDER_FIELD]

    data          = json_message[topic]
    timestamp     = json_message[Common.TIMESTAMP_FIELD]
    snapshot_id   = json_message[Common.SNAPSHOT_ID_FIELD]
    snapshot_path = json_message[Common.SNAPSHOT_PATH_FIELD]

    user_entry = UserEntry(user_id=user_id, username=username, birthdate=birthdate, gender=gender)
    result_entry = ResultEntry(user_id=user_id, snapshot_id=snapshot_id, snapshot_path=snapshot_path,
                               timestamp=timestamp, result_type=topic, result_data=data)

    mongo_handler.save_user(user_entry=user_entry)
    mongo_handler.save_snapshot_result(result_entry=result_entry)


if __name__ == '__main__':
    main()
