from Anthon.parsers.BaseParser import BaseParser
from Anthon.parsers import Session


class FeelingsParser(BaseParser):

    parser_type = "feelings"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)
        feelings_json = {
            'hunger':     snapshot.feelings.hunger,
            'thirst':     snapshot.feelings.thirst,
            'exhaustion': snapshot.feelings.exhaustion,
            'happiness':  snapshot.feelings.happiness,
        }

        return {self.parser_type: feelings_json}

    def __init__(self):
        super().__init__()
