from Anton.anthon_pb2 import Snapshot
from pathlib import Path
from Anton.parsers import Session
from abc import ABC, abstractmethod


class BaseParser(ABC):

    parser_type = "base"

    def __init__(self):
        pass

    @abstractmethod
    def parse(self, path, session: Session):
        pass

    @staticmethod
    def get_snapshot_data(path):
        file = Path(path)
        if file.is_file():
            data = file.read_bytes()
            snapshot = Snapshot()
            snapshot.ParseFromString(data)
        else:
            raise FileNotFoundError("No such file " + path)

        return snapshot
