import click
from furl import furl
from .MongoHandler import MongoHandler, MONGO_DEFAULT_PATH


@click.group()
def main():
    pass


@main.command()
@click.option("--database", "-d", default=MONGO_DEFAULT_PATH)
@click.argument('topic')
@click.argument('path')
def save(database, topic, path):

    url = furl(database)
    if url.scheme != "mongodb":
        raise Exception(f'Only database supported is mongodb, ({url.scheme} is not supported)')

    mongo_handler = MongoHandler(path=url.path)



if __name__ == '__main__':
    main()
