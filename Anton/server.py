import click
from flask import Flask, jsonify, request
from Anton.anthon_pb2 import ServerMessage, User
from uuid import uuid4
from pathlib import Path
from Anton.mq_handler import MQHandler, UnsupportedSchemeException
import json
import Anton.common as Common
from Anton.common import bcolors


ERRNO_PERMISSION_DENIED = -2
ERRNO_UNSUPPORTED_SCHEME = -3


app = Flask(__name__)
_publish = None
SNAPSHOTS_DIRECTORY = "./snapshots"


@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('publish')
def run_server_cli(host, port, publish):
    run_server(host=host, port=port, publish=publish)


def run_server(host, port, publish):
    global _publish
    _publish = publish
    try:
        app.run(host=host, port=port)
    except PermissionError:
        print(f'{bcolors.FAIL}ERROR: Can\'t bind server to {host}:{port}{bcolors.ENDC}')
        exit(ERRNO_PERMISSION_DENIED)

    print(f'host={host}, port={port}, publish={publish}')


@app.route('/user', methods=['POST'])
def new_user():
    data = request.data
    user = User.FromString(data)

    user_id   = user.user_id
    username  = user.username
    birthdate = user.birthdate
    gender    = user.gender

    data = {
        Common.USER_ID_FIELD:   user_id,
        Common.USERNAME_FIELD:  username,
        Common.BIRTHDATE_FIELD: birthdate,
        Common.GENDER_FIELD:    gender,
    }

    user_message = {Common.TYPE_FIELD: Common.USER_TYPE, Common.DATA_FIELD: data}
    publish_user(json.dumps(user_message))


@app.route('/msg', methods=['POST'])
def new_message():
    data = request.data

    msg = ServerMessage()
    msg.ParseFromString(data)

    user_data     = msg.user
    user_id       = user_data.user_id
    username      = user_data.username
    birthdate     = user_data.birthday
    gender        = user_data.gender
    snapshot_data = msg.snapshot
    timestamp     = msg.snapshot.datetime

    snapshot_id = uuid4().hex
    snapshot_path = save_snapshot_to_disk(snapshot_data, snapshot_id)

    message_dict = {
        Common.USER_ID_FIELD:       user_id,
        Common.USERNAME_FIELD:      username,
        Common.BIRTHDATE_FIELD:     birthdate,
        Common.GENDER_FIELD:        gender,
        Common.SNAPSHOT_ID_FIELD:   snapshot_id,
        Common.SNAPSHOT_PATH_FIELD: snapshot_path,
        Common.TIMESTAMP_FIELD:     timestamp,
    }
    _save_message_to_disk(message_dict)

    publish_message(message=json.dumps(message_dict))
    return jsonify(message_dict)


def publish_message(message):
    if callable(_publish):
        _publish(message)
        return

    try:
        mq_handler = MQHandler(_publish)
        mq_handler.to_parsers(message)
    except UnsupportedSchemeException as e:
        print(f'{bcolors.FAIL}ERROR: Publisher {e.scheme} is not supported{bcolors.ENDC}')
        exit(ERRNO_UNSUPPORTED_SCHEME)


def publish_user(message):
    if callable(_publish):
        _publish(message)
        return

    mq_handler = MQHandler(_publish)
    mq_handler.to_saver(message)


def save_snapshot_to_disk(snapshot_data, snapshot_id):
    # TODO: make sure that directory exists
    file = Path(SNAPSHOTS_DIRECTORY) / (snapshot_id  + ".snp")
    file.write_bytes(snapshot_data.SerializeToString())

    return str(file.absolute())


# For debugging only
def _save_message_to_disk(message_data):
    file = Path(SNAPSHOTS_DIRECTORY) / (message_data['snapshot_id'] + ".raw")
    file.write_text(json.dumps(message_data))


if __name__ == '__main__':
    main()
