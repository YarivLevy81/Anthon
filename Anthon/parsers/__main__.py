import click
from .PoseParser import PoseParser
from .FeelingsParser import FeelingsParser
from .ColorImageParser import ColorImageParser
from .DepthImageParser import DepthImageParser


@click.group()
def main():
    pass


@main.command()
@click.argument('parser_type')
@click.argument('path')
def parse(parser_type, path):
    parser = init_parser_type(parser_type)
    parser.parse()

    print("Parsing..")


@main.command()
@click.argument('parser_type')
@click.argument('path')
@click.argument('publisher')
def run_parser(parser_type, path, publisher):
    print("Running parser..")


def init_parser_type(parser_type: str):
    parser_type = parser_type.lower()
    if parser_type == PoseParser.parser_type:
        return PoseParser()

    if parser_type == FeelingsParser.parser_type:
        return FeelingsParser()

    if parser_type == DepthImageParser.parser_type:
        return DepthImageParser()

    if parser_type == ColorImageParser.parser_type:
        return ColorImageParser()


if __name__ == '__main__':
    main()
