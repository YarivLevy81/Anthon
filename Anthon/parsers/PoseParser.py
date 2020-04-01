from Anthon.parsers.BaseParser import BaseParser


class PoseParser(BaseParser):

    parser_type = "pose"

    def parse(self, path):
        snapshot = self.get_snapshot_data(path)
        translation = snapshot.pose.translation
        rotation = snapshot.pose.rotation


    def __init__(self):
        super().__init__()
