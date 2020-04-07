import click
from flask import Flask, jsonify, request
from PIL import Image
from anthon_pb2 import ServerMessage
from uuid import uuid4
from pathlib import Path
from .mq_handler import MQHandler


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


@app.route('/msg', methods=['POST'])
def new_message():
    data = request.data
    msg = ServerMessage()
    msg.ParseFromString(data)

    user_data = msg.user
    snapshot_data = msg.snapshot

    snapshot_id = uuid4().hex
    snapshot_path = save_snapshot_to_disk(snapshot_data, snapshot_id)

    message_dict = dict(
        path=snapshot_path,
        user_data=user_data,
        snapshot_id=snapshot_id
    )

    publish_message(message=message_dict)
    return jsonify(message_dict)


def publish_message(message):
    if callable(_publish):
        _publish(message)
        return

    mq_handler = MQHandler(_publish)
    mq_handler.to_parsers(message)


def save_snapshot_to_disk(snapshot_data, snapshot_id):
    file = Path(SNAPSHOTS_DIRECTORY) / snapshot_id + ".raw"
    file.write_bytes(snapshot_data)

    return file.absolute()


if __name__ == '__main__':
    main()
