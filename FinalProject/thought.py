from datetime import datetime
import struct

class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id   = user_id
        self.timestamp = timestamp
        self.thought   = thought

    def __repr__(self):
        out_string = f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'
        return out_string

    def __str__(self):
        date_out = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        out_string = f'[{date_out}] user {self.user_id}: {self.thought}'
        return out_string

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        serialized = struct.pack("<Q", self.user_id)
        serialized += struct.pack("<Q", int(self.timestamp.timestamp()))
        serialized += b'\n\x00\x00\x00'
        serialized += self.thought.strip().encode()
        return serialized

    @staticmethod
    def deserialize(serialized):
        user_id   = int.from_bytes(serialized[:8], byteorder="little")
        timestamp = datetime.fromtimestamp(int.from_bytes(serialized[8:16], byteorder="little"))
        thought   = serialized[20:].decode().strip()
        return Thought(user_id, timestamp, thought)
