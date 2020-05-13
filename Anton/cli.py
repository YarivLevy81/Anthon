import requests
import click
import pathlib


HTTP_SCHEME = "http"


@click.group()
def main():
    pass


@main.command("get-users")
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
def get_users(host, port):
    request_url = f'{HTTP_SCHEME}://{host}:{port}/users'
    r = requests.get(url=request_url)

    print(r.json())
    return r.json()


@main.command("get-user")
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
@click.argument("user_id")
def get_user(host, port, user_id):
    request_url = f'{HTTP_SCHEME}://{host}:{port}/users/{user_id}'
    r = requests.get(url=request_url)

    print(r.json())
    return r.json()


@main.command("get-snapshots")
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
@click.argument("user_id")
def get_snapshots(host, port, user_id):
    request_url = f'{HTTP_SCHEME}://{host}:{port}/users/{user_id}/snapshots'
    r = requests.get(url=request_url)

    print(r.json())
    return r.json()


@main.command("get-snapshot")
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
@click.argument("user_id")
@click.argument("snapshot_id")
def get_snapshot(host, port, user_id, snapshot_id):
    request_url = f'{HTTP_SCHEME}://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    r = requests.get(url=request_url)

    print(r.json())
    return r.json()


@main.command("get-result")
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=5000)
@click.argument("user_id")
@click.argument("snapshot_id")
@click.argument("topic")
@click.option('--save', '-s')
def get_result(host, port, user_id, snapshot_id, topic, save):
    request_url = f'{HTTP_SCHEME}://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{topic}'
    r = requests.get(url=request_url)

    if save:
        path = pathlib.Path(save)
        path.write_text(r.text)

    print(r.json())
    return r.json()


if __name__ == '__main__':
    main()
