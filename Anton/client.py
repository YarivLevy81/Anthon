from Anton.snapshot_reader import SampleReader
from Anton.anthon_pb2 import ServerMessage
import click
import requests
import pathlib
from Anton.common import bcolors


ERRNO_FILE_NOT_EXIST = -2
ERRNO_FILE_NOT_GZIP = -3
ERRNO_SERVER_UNAVAILABLE = -4


@click.group()
def main():
    pass


@main.command('upload-sample')
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8000)
@click.argument('path')
def upload_sample_cli(host, port, path):
    upload_sample(host=host, port=port, path=path)


def upload_sample(host, port, path):
    print(f'Uploading sample - host={host}, port={port}, path={path}')

    if not pathlib.Path(path).exists() or not pathlib.Path(path).is_file():
        print(f'{bcolors.FAIL}ERROR: No such file {path} {bcolors.ENDC}')
        exit(ERRNO_FILE_NOT_EXIST)

    if not is_gz_file(path):
        print(f'{bcolors.FAIL}ERROR: File {path} is not .gz formatted {bcolors.ENDC}')
        exit(ERRNO_FILE_NOT_GZIP)

    rdr = SampleReader(path)

    # We will now iterate the reader, and send every snapshot to the server
    for snapshot in rdr:

        msg = ServerMessage()
        populate_message(msg, rdr, snapshot)
        try:
            r = requests.post(f'http://{host}:{port}/msg',
                              headers={'Content-Type': 'application/protobuf'},
                              data=msg.SerializeToString())

        except requests.exceptions.RequestException as e:
            print(f'{bcolors.FAIL}ERROR: Connectivity problem with {host}:{port}\nStackTrace -\n{e}{bcolors.ENDC}')
            exit(ERRNO_SERVER_UNAVAILABLE)


def populate_message(msg, reader, snapshot):
    msg.user.CopyFrom(reader.user)
    msg.snapshot.CopyFrom(snapshot)


def is_gz_file(path):
    import binascii

    def _is_gz_file():
        with open(path, 'rb') as test_f:
            return binascii.hexlify(test_f.read(2)) == b'1f8b'
    return _is_gz_file()


if __name__ == '__main__':
    main()
