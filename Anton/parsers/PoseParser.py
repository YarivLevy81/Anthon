from Anton.parsers.BaseParser import BaseParser
from Anton.parsers import Session


class PoseParser(BaseParser):

    parser_type = "pose"

    def parse(self, path, session: Session):
        snapshot = self.get_snapshot_data(path)
        pose_json = {
            'translation_x': snapshot.pose.translation.x,
            'translation_y': snapshot.pose.translation.y,
            'translation_z': snapshot.pose.translation.z,

            'rotation_x': snapshot.pose.rotation.x,
            'rotation_y': snapshot.pose.rotation.y,
            'rotation_z': snapshot.pose.rotation.z,
            'rotation_w': snapshot.pose.rotation.w,
        }

        return {self.parser_type: pose_json}

    def __init__(self):
        super().__init__()
