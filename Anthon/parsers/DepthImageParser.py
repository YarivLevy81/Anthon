from Anthon.parsers.BaseParser import BaseParser
from Anthon.parsers import Session
import matplotlib.pyplot as plt
import numpy as np


class DepthImageParser(BaseParser):

    parser_type = "depth_image"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)
        data = np.array(list(snapshot.depth_image.data))
        data = data.reshape([snapshot.depth_image.height, snapshot.depth_image.width])
        plt.imshow(data, cmap='hot', interpolation='nearest')

        image_path = session.new_path(self.parser_type + '.png')
        plt.savefig(image_path)
        json_data = {
            'height':     snapshot.color_image.height,
            'width':      snapshot.color_image.width,
            'image_path': image_path
        }

        return {self.parser_type: json_data}

    def __init__(self):
        super().__init__()
