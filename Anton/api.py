from flask import Flask, send_file
import click
from Anton.saver.MongoHandler import MongoHandler
import json
from Anton.common import *

app = Flask(__name__)
_database = None
headers = {"Content-Type": "application/json"}

ERRNO_PERMISSION_DENIED = -2


@click.group()
def main():
    pass


@main.command('run-server')
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
@click.option('--database', "-d", default="mongodb://127.0.0.1:27017")
def run_server(host, port, database):
    run_api_server(host=host, port=port, database=database)


def run_api_server(host, port, database):
    global _database
    _database = MongoHandler(database)
    try:
        app.run(host=host, port=port)
    except PermissionError:
        print(f'{bcolors.FAIL}ERROR: Can\'t bind server to {host}:{port}{bcolors.ENDC}')
        exit(ERRNO_PERMISSION_DENIED)


@app.route("/users", methods=['GET'])
def get_users():
    users_json = _database.get_all_users()

    response = app.response_class(
        response=json.dumps(users_json),
        mimetype='application/json'
    )

    return response


@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user_json = _database.get_user(user_id)
    if user_json is None:
        user_json = {}

    response = app.response_class(
        response=json.dumps(user_json),
        mimetype='application/json'
    )

    return response


@app.route("/users/<int:user_id>/snapshots", methods=['GET'])
def get_user_snapshots(user_id):
    snapshots_json = _database.get_user_snapshots(user_id)
    if snapshots_json is None:
        snapshots_json = []

    response = app.response_class(
        response=json.dumps(snapshots_json),
        mimetype='application/json'
    )

    return response


@app.route("/users/<int:user_id>/snapshots/<snapshot_id>", methods=['GET'])
def get_user_snapshot(user_id, snapshot_id):
    snapshot_json = _database.get_snapshot(user_id=user_id, snapshot_id=snapshot_id)
    if snapshot_json is None:
        snapshot_json = {}

    response = app.response_class(
        response=json.dumps(snapshot_json),
        mimetype='application/json'
    )

    return response


@app.route("/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>", methods=['GET'])
def get_user_snapshot_result(user_id, snapshot_id, result_name):
    result_json = base_user_snapshot_result(user_id=user_id, snapshot_id=snapshot_id, result_name=result_name)

    response = app.response_class(
        response=json.dumps(result_json),
        mimetype='application/json'
    )

    return response


@app.route("/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>/data", methods=['GET'])
def get_user_snapshot_result_data(user_id, snapshot_id, result_name):
    result_json = base_user_snapshot_result(user_id=user_id, snapshot_id=snapshot_id, result_name=result_name)
    if IMAGE_PATH_FIELD in result_json:
        image_path = result_json[IMAGE_PATH_FIELD]
        return send_file(image_path, mimetype='image/png')

    else:
        result_json = {}

        response = app.response_class(
            response=json.dumps(result_json),
            mimetype='application/json'
        )
        return response


def base_user_snapshot_result(user_id, snapshot_id, result_name):
    result_json = _database.get_snapshot_result(user_id=user_id, snapshot_id=snapshot_id, topic=result_name)
    if result_json is None:
        result_json = {}

    return result_json


if __name__ == '__main__':
    main()
