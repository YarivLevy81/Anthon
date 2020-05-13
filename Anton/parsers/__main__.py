import click
from Anton.parsers import run_parser, parse


@click.group()
def main():
    pass


@main.command('parse')
@click.argument('parser_type')
@click.argument('path')
def parse_cli(parser_type, path):
    return parse(parser_type=parser_type, path=path)


@main.command('run-parser')
@click.argument('parser_type')
@click.argument('publisher')
def run_parser_cli(parser_type, publisher):
    run_parser(parser_type=parser_type, publisher=publisher)


if __name__ == '__main__':
    main()
