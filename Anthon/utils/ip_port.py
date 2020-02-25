import socket


def formatted_address(address):
    address = address.split(":")
    socket.inet_aton(address[0])
    if (int(address[1]) < 0) and (int(address[1]) > 65535):
        raise ValueError("Port is out of range or not a number")
    address[1] = int(address[1])

    return address[0], address[1]
