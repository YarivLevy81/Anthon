import click
from furl import furl
from .MongoHandler import MongoHandler, MONGO_DEFAULT_PATH
from Anthon.mq_handler import MQHandler, UnsupportedSchemeException
import json


@click.group()
def main():
    pass


@main.command()
@click.option("--database", "-d", default=MONGO_DEFAULT_PATH)
@click.argument('topic')
@click.argument('path')
def save(database, topic, path):

    url = furl(database)
    if url.scheme != "mongodb":
        raise UnsupportedSchemeException(f'Only database supported is mongodb, ({url.scheme} is not supported)')
    mongo_handler = MongoHandler(path=url.path)

    file = open(path, 'rb')
    json_message = json.loads(file.read())
    data = json_message['data']
    user_id = json_message['user_id']
    timestamp = json_message['timestamp']
    snapshot_id = json_message['snapshot_id']
    snapshot_path = json_message['snapshot_path']


if __name__ == '__main__':
    main()
