import socket
import time
import datetime
import struct
from utils.connection import Connection


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
    
        address = address.split(":")
        socket.inet_aton(address[0])
        if (int(address[1]) < 0) and (int(address[1]) > 65535):
            raise ValueError
        address[1] = int(address[1])
        
        user_id = int(user_id)
        
        upload_thought(address, user_id, thought)

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
