from Anton.anthon_pb2 import QueueMessage, Snapshot
from pathlib import Path
import json
from Anton.parsers import Session


class BaseParser:

    parser_type = "base"

    def __init__(self):
        pass

    def parse(self, path, session: Session):
        raise NotImplementedError()

    def run_parser(self):
        pass

    def get_snapshot_data(self, path):
        file = Path(path)
        if file.is_file():
            data = file.read_bytes()
            snapshot = Snapshot()
            snapshot.ParseFromString(data)
        else:
            raise Exception("No such file " + path)

        return snapshot

    def message_callback(self, path):
        # Integrate with RabitMQ

        file = Path(path)
        if file.is_file():
            with open(path) as json_file:
                data = json.load(json_file)
        else:
            raise Exception("No file " + path)

        return data
