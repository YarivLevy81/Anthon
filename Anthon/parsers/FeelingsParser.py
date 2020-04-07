from Anthon.parsers.BaseParser import BaseParser
import json
from . import Session


class FeelingsParser(BaseParser):

    parser_type = "feeling"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)
        pose_json = {
            'hunger':     snapshot.feelings.hunger,
            'thirst':     snapshot.feelings.thirst,
            'exhaustion': snapshot.feelings.exhaustion,
            'happiness':  snapshot.feelings.happiness,
        }

        return json.dumps({"data": pose_json})

    def __init__(self):
        super().__init__()
