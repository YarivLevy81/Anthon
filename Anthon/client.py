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
    rdr = SampleReader(path)

    print(f'host={host}, port={port}, path={path}')

    print(rdr.user_id)
    snp = next(rdr)
    img = snp
    msg = ServerMessage()
    populate_message(msg, rdr, snp)
    print(len(msg.SerializeToString()))
    r = requests.post(f'http://{host}:{port}/msg',
                      headers={'Content-Type': 'application/protobuf'},
                      data=msg.SerializeToString())
    print(r.text)


def populate_message(msg, reader, snapshot):
    msg.user.CopyFrom(reader.user)
    msg.snapshot.CopyFrom(snapshot)


if __name__ == '__main__':
    main()
