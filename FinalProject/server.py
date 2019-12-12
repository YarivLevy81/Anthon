import time
import datetime
import struct
import threading

from utils.ip_port import formatted_address
from utils.listener import Listener


def run_server(address):
    listener = Listener(address[1], address[0])
    listener.start()

    while True:
        conn = listener.accept()
        threading._start_new_thread(new_client, (conn,))


def new_client(conn):
    time.sleep(1)

    from_client = bytes()
    while True:
        data = conn.receive(1024)
        if not data:
            break
        from_client += data

    pk = from_client
    pk_tup = struct.unpack("<qqi", pk[:20])

    user_id      = pk_tup[0]
    timestamp    = pk_tup[1]
    thought_size = pk_tup[2]
    thought      = pk[20:]
    thought      = thought.decode()

    datetime_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    log_string = "["
    log_string += datetime_string
    log_string += "]"
    log_string += " user "
    log_string += str(user_id)
    log_string += ": "
    log_string += thought

    print(log_string)

    conn.close()


def main(argv):
    if len(argv) != 2:
        print(f'USAGE: {argv[0]} <address>')
        return 1
    try:
        address = argv[1]

        # IP:Port manipulation
        address = formatted_address(address)

        run_server(address)

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
