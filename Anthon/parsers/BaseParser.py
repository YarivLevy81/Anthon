from anthon_pb2 import QueueMessage, Snapshot
from pathlib import Path
import json

class BaseParser:

    parser_type = "base"

    def __init__(self):
        pass

    def parse(self, path):
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
            raise Exception("No file " + path)

        return snapshot

    def extract_message(self, path):
        # Integrate with RabitMQ

        file = Path(path)
        if file.is_file():
            with open(path) as json_file:
                data = json.load(json_file)
        else:
            raise Exception("No file " + path)

        return data
