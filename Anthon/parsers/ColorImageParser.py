from Anthon.parsers.BaseParser import BaseParser


class ColorImageParser(BaseParser):

    parser_type = "color_image"

    def parse(self, path):
        snapshot = self.get_snapshot_data(path)



    def __init__(self):
        super().__init__()
