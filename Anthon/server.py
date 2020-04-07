import click
from flask import Flask, jsonify, request
from .anthon_pb2 import ServerMessage, User
from uuid import uuid4
from pathlib import Path
from .mq_handler import MQHandler
import json
import Anthon.common as Common


app = Flask(__name__)
_publish = None
SNAPSHOTS_DIRECTORY = "/snapshots"


@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('publish')
def run_server(host, port, publish):
    global _publish
    _publish = publish
    app.run(host=host, port=port)

    print(f'host={host}, port={port}, publish={publish}')


@app.route('/user', methods=['POST'])
def new_user():
    data = request.data
    user = User.FromString(data)

    user_id = user.user_id
    username = user.username
    birthdate = user.birthdate
    gender = user.gender

    data = {
        Common.USER_ID_FIELD: user_id,
        Common.USERNAME_FIELD: username,
        Common.BIRTHDATE_FIELD: birthdate,
        Common.GENDER_FIELD: gender,
    }

    user_message = {Common.TYPE_FIELD: Common.USER_TYPE, Common.DATA_FIELD: data}
    publish_user(json.dumps(user_message))


@app.route('/msg', methods=['POST'])
def new_message():
    data = request.data
    msg = ServerMessage()
    msg.ParseFromString(data)

    user_data = msg.user
    user_id = user_data.user_id
    snapshot_data = msg.snapshot
    timestamp = msg.snapshot.timestamp

    snapshot_id = uuid4().hex
    snapshot_path = save_snapshot_to_disk(snapshot_data, snapshot_id)

    message_dict = {
        Common.SNAPSHOT_PATH_FIELD: snapshot_path,
        Common.USER_ID_FIELD: user_id,
        Common.SNAPSHOT_ID_FIELD: snapshot_id,
        Common.TIMESTAMP_FIELD: timestamp,
    }

    publish_message(message=json.dumps(message_dict))
    return jsonify(message_dict)


def publish_message(message):
    if callable(_publish):
        _publish(message)
        return

    mq_handler = MQHandler(_publish)
    mq_handler.to_parsers(message)


def publish_user(message):
    if callable(_publish):
        _publish(message)
        return

    mq_handler = MQHandler(_publish)
    mq_handler.to_saver(message)


def save_snapshot_to_disk(snapshot_data, snapshot_id):
    file = Path(SNAPSHOTS_DIRECTORY) / snapshot_id + ".raw"
    file.write_bytes(snapshot_data)

    return file.absolute()


if __name__ == '__main__':
    main()
