import socket
import time
import datetime
import struct
import threading


def run_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address[0], address[1]))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        threading._start_new_thread(new_client,(conn,addr))


def new_client(conn, addr):
        time.sleep(1)
        
        from_client = bytes()
        while True:
            data = conn.recv(1024)
            if not data: break
            from_client += data

        pk = from_client
        pk = struct.unpack("<qqi{0}s".format(len(from_client) - 20), pk)

        user_id      = pk[0]
        timestamp    = pk[1]
        thought_size = pk[2]
        thought      = pk[3]
        thought      = thought.decode()
        
        datetime_string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        log_string =  "["
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
        
        address = address.split(":")
        socket.inet_aton(address[0])
        if (int(address[1]) < 0) or (int(address[1]) > 65535):
            raise ValueError
        address[1] = int(address[1])

        run_server(address)
        
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
