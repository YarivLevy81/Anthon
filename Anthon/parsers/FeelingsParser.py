from Anthon.parsers.BaseParser import BaseParser
from anthon_pb2 import Snapshot

class FeelingsParser(BaseParser):

    parser_type = "feeling"

    def parse(self, path):
        snapshop = Snapshot()

    def __init__(self):
        super().__init__()
