import socket


class Connection:

    def __init__(self, sock):
        print(1)
        self.socket = sock

    def __enter__(self):
        print('hey')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('hello')
        print(exc_type, exc_val, exc_tb)
        self.close()

    def __repr__(self):
        host = self.socket.getsockname()
        peer = self.socket.getpeername()
        out_string = f'<Connection from {host[0]}:{host[1]!r} to {peer[0]}:{peer[1]!r}>'
        return out_string

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data_in = self.socket.recv(size)
        if len(data_in) != size:
            raise socket.error(f'Expected to receive {size} bytes but got {len(data_in)}')
        return data_in

    def close(self):
        self.socket.close()

    @classmethod
    def connect(cls, addr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((addr, port))
        return cls(sock)
