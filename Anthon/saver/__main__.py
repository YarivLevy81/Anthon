import click
from Anthon.saver.MongoHandler import MONGO_DEFAULT_PATH
from Anthon.saver import run_saver, save


@click.group()
def main():
    pass


@main.command('run-saver')
@click.argument('database')
@click.argument('publisher')
def run_saver_cli(database, publisher):
    run_saver(database=database, publisher=publisher)


@main.command('save')
@click.option("--database", "-d", default=MONGO_DEFAULT_PATH)
@click.argument('topic')
@click.argument('path')
def save_cli(database, topic, path):
    save(database=database, topic=topic, path=path)


if __name__ == '__main__':
    main()
