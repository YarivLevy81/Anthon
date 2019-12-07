import socket
import time
import datetime
import struct

def upload_thought(address, user_id, thought):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((address[0], address[1]))

    #packet =  (user_id).to_bytes(8, byteorder='little')
    #packet += (int(time.time())).to_bytes(8, byteorder='little')
    #packet += (len(thought)).to_bytes(8, byteorder='little').strip()
    #packet += thought.encode()[::-1]
    packet = struct.pack("<qqi{0}s".format(len(thought)), user_id, int(time.time()), len(thought), thought.encode())
    #print(packet)
    
    clientsocket.sendall(packet)


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
        
        print('done')
    #except socket.error:
        #print("{arg[1]} - Address string is not valid IP:Port")
        #return 1
    #except ValueError:
        #print("{arg[2]} - String is not valid int")
        #return 1
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
