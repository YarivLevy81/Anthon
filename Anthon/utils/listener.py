from utils.connection import Connection
import socket


class Listener:

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = None

    def __repr__(self):
        out_string = f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'
        return out_string

    def start(self):
        self.socket = socket.socket()
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def stop(self):
        self.socket.close()

    def accept(self):
        conn, addr = self.socket.accept()
        return Connection(conn)
