import socket
import time
import struct
from utils.connection import Connection
from utils.ip_port import formatted_address


def upload_thought(address, user_id, thought):
    conn = Connection.connect(address[0], address[1])

    packet = struct.pack("<qqi".format(len(thought)), user_id, int(time.time()), len(thought))
    packet += thought.encode()

    conn.send(packet)


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        address = argv[1]
        user_id = argv[2]
        thought = argv[3]

        # IP:Port manipulation
        address = formatted_address(address)
        
        user_id = int(user_id)
        
        upload_thought(address, user_id, thought)

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
