from protocol import Snapshot
import struct
from PIL import Image

SIZE_OF_DOUBLE = 8
SIZE_OF_LONG = 8
SIZE_OF_FLOAT = 4
SIZE_OF_INT = 4

# TODO: 1) Handle errors, 2) Handle stop iterations


class BaseReader:
    def __init__(self, path, on_create=None):
        self.path = path
        self.f = open(path, 'rb')
        if on_create is not None:
            on_create()


class SampleReader(BaseReader):

    def __init__(self, path):
        self.user_id = -1
        self.username = ""
        self.birth_date = -1
        self.gender = ''
        super().__init__(path, self.read_user_information)

    def read_user_information(self):
        user_id_in_bytes = self.f.read(8)
        self.user_id = int.from_bytes(user_id_in_bytes, byteorder='little')

        user_name_length_in_bytes = self.f.read(4)
        user_name_length = int.from_bytes(user_name_length_in_bytes, byteorder='little')
        user_name_in_bytes = self.f.read(user_name_length)
        self.username = user_name_in_bytes.decode()

        birth_date_in_bytes = self.f.read(4)
        self.birth_date = int.from_bytes(birth_date_in_bytes, byteorder='little')

        gender_in_bytes = self.f.read(1)
        self.gender = int.from_bytes(gender_in_bytes, byteorder='little')

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_snapshot()

    def next_snapshot(self):
        snapshot = Snapshot()

        snapshot.timestamp = int.from_bytes(self.f.read(8), byteorder='little')

        translation_unpacked = struct.unpack('ddd', self.f.read(3*SIZE_OF_DOUBLE))
        snapshot.translation.x = translation_unpacked[0]
        snapshot.translation.y = translation_unpacked[1]
        snapshot.translation.z = translation_unpacked[2]

        rotation_unpacked = struct.unpack('dddd', self.f.read(4*SIZE_OF_DOUBLE))
        snapshot.rotation.x = rotation_unpacked[0]
        snapshot.rotation.y = rotation_unpacked[1]
        snapshot.rotation.z = rotation_unpacked[2]
        snapshot.rotation.w = rotation_unpacked[3]

        color_image_height = int.from_bytes(self.f.read(SIZE_OF_INT), byteorder='little')
        color_image_width = int.from_bytes(self.f.read(SIZE_OF_INT), byteorder='little')
        color_image_in_bytes = self.f.read(color_image_height * color_image_width * 3)
        snapshot.color_image = Image.frombytes('RGB', (color_image_width, color_image_height), color_image_in_bytes, 'raw')
        b, g, r = snapshot.color_image.split()
        snapshot.color_image = Image.merge('RGB', (r, g, b))

        depth_image_height = int.from_bytes(self.f.read(SIZE_OF_INT), byteorder='little')
        depth_image_width = int.from_bytes(self.f.read(SIZE_OF_INT), byteorder='little')
        depth_image_in_bytes = self.f.read(depth_image_height * depth_image_width * SIZE_OF_FLOAT)
        snapshot.depth_image = Image.frombytes('F', (depth_image_width, depth_image_height), depth_image_in_bytes, 'raw')

        feeling_unpacked = struct.unpack('ffff', self.f.read(4 * SIZE_OF_FLOAT))
        snapshot.feelings.hunger = feeling_unpacked[0]
        snapshot.feelings.thirst = feeling_unpacked[1]
        snapshot.feelings.exhaustion = feeling_unpacked[2]
        snapshot.feelings.happiness = feeling_unpacked[3]

        return snapshot
