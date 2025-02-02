import click
import Anton.gui.app as gui_app
from Anton.common import bcolors


ERRNO_PERMISSION_DENIED = -2


@click.group()
def main():
    pass


def run_gui_server(host, port, api_host, api_port):
    app = gui_app.create_app()
    app.config['host'] = host
    app.config['port'] = port
    app.config['api_host'] = api_host
    app.config['api_port'] = api_port

    try:
        app.run(host=host, port=port)
    except PermissionError:
        print(f'{bcolors.FAIL}ERROR: Can\'t bind server to {host}:{port}{bcolors.ENDC}')
        exit(ERRNO_PERMISSION_DENIED)


@main.command('run-server')
@click.option("--host", "-h", default='127.0.0.1')
@click.option("--port", "-p", default=8080)
@click.option("--api-host", "-H", default='127.0.0.1')
@click.option("--api-port", "-P", default=5000)
def run_server(host, port, api_host, api_port):
    run_gui_server(host=host, port=port, api_host=api_host, api_port=api_port)


if __name__ == '__main__':
    main()
