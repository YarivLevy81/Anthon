import click
from flask import Flask, jsonify, request
from PIL import Image
from anthon_pb2 import Message

app = Flask(__name__)
_publish = None


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
    msg = Message()
    msg.ParseFromString(data)
    img = msg.snapshot.color_image
    Image.frombytes('RGB', (img.width, img.height), img.data, 'raw').show()

    return jsonify({'new_message': 1})


if __name__ == '__main__':
    main()
