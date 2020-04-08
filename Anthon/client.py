import click
from snapshot_reader import SampleReader
from anthon_pb2 import ServerMessage
from PIL import Image
import requests


@click.group()
def main():
    pass


@main.command()
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('path')
def upload_sample(host, port, path):
    print(f'host={host}, port={port}, path={path}')

    rdr = SampleReader(path)

    # We first send the user
    r = requests.post(f'http://{host}:{port}/user',
                      headers={'Content-Type': 'application/protobuf'},
                      data=rdr.user.SerializeToString())
    # TODO: Check result and exit gracefully
    print(f'user_id={rdr.user_id})')

    # We will now iterate the reader, and send every snapshot to the server
    for snapshot in rdr:

        msg = ServerMessage()
        populate_message(msg, rdr, snapshot)
        r = requests.post(f'http://{host}:{port}/msg',
                          headers={'Content-Type': 'application/protobuf'},
                          data=msg.SerializeToString())
        print(f'response={r.text}')


def populate_message(msg, reader, snapshot):
    msg.user.CopyFrom(reader.user)
    msg.snapshot.CopyFrom(snapshot)


if __name__ == '__main__':
    main()
