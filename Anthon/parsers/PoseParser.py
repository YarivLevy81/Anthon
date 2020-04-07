from Anthon.parsers.BaseParser import BaseParser
import json
from . import Session


class PoseParser(BaseParser):

    parser_type = "pose"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)
        pose_json = {
            'translation_x': snapshot.pose.translation.x,
            'translation_y': snapshot.pose.translation.y,
            'translation_z': snapshot.pose.translation.z,

            'rotation_x': snapshot.rotation.x,
            'rotation_y': snapshot.rotation.y,
            'rotation_z': snapshot.rotation.z,
            'rotation_w': snapshot.rotation.w,
        }

        return json.dumps({"data": pose_json})

    def __init__(self):
        super().__init__()
