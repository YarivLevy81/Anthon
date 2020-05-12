from Anthon.parsers.BaseParser import BaseParser
from PIL import Image
from Anthon.parsers import Session


class ColorImageParser(BaseParser):

    parser_type = "color_image"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)

        size = snapshot.color_image.width, snapshot.color_image.height
        data = snapshot.color_image.data
        image = Image.frombytes(data=data, mode='RGB', size=size)
        image_path = session.new_path(self.parser_type + '.png')
        image.save(image_path, "PNG")

        json_data = {
            'height':       snapshot.color_image.height,
            'width':        snapshot.color_image.width,
            'image_path':   image_path
        }

        return {self.parser_type: json_data}

    def __init__(self):
        super().__init__()
