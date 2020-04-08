from anthon_pb2 import User, Snapshot
import struct
from PIL import Image
import gzip

SIZE_OF_DOUBLE = 8
SIZE_OF_LONG = 8
SIZE_OF_FLOAT = 4
SIZE_OF_INT = 4
MSG_SIZE = 4

# TODO: 1) Handle errors, 2) Handle stop iterations


class BaseReader:
    def __init__(self, path, on_create=None):
        if on_create is not None:
            on_create()


class SampleReader(BaseReader):
    """
    :param user_id: id number of the user
    """
    def __init__(self, path, byteorder='little'):
        self.path = path
        self.file = gzip.open(self.path)
        self.byteorder = byteorder
        #TODO: Handle exception here

        self.user       = None
        self.user_id    = -1
        self.username   = ""
        self.birth_date = -1
        self.gender     = ''

        super().__init__(path, self.read_user_information)

    def read_user_information(self):
        user_msg_size_bytes = self.file.read(MSG_SIZE)
        user_msg_size = int.from_bytes(user_msg_size_bytes, byteorder=self.byteorder)

        user_data_bytes = self.file.read(user_msg_size)
        user = User.FromString(user_data_bytes)
        self.user       = user
        self.user_id    = user.user_id
        self.username   = user.username
        self.birth_date = user.birthday
        self.gender     = user.gender

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_snapshot()

    def next_snapshot(self):
        msg_size_bytes = self.file.read(MSG_SIZE)
        msg_size = int.from_bytes(msg_size_bytes, byteorder=self.byteorder)

        msg_bytes = self.file.read(msg_size)
        snapshot = Snapshot.FromString(msg_bytes)
        return snapshot
