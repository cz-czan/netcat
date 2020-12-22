import sys
import socket
import getopt
from utils import *

server_address = ""
server_port = 0



try:
    opts, args = getopt.getopt(sys.argv[1:],"t:p:",["target","port"])

    for o, v in opts: # o - option; v - value
        if o in ("-t", "--target"):
            server_address = v
        if o in ("-p", "--port"):
            server_port = int(v)
except getopt.GetoptError as err:
    print(str(err))

print("Creating TCP/IPv6 socket")
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
print("Connecting with " + str(server_address) + " on port " + str(server_port))
print(s.connect((server_address, server_port)))
print("Connection established")
print(receive(s, 1024).decode('utf-8'), end='', flush=True) # Waiting for the console prefix ( 16 bytes max ) and printing
def main():
    for n, line in enumerate(sys.stdin):
        if(len(line) < 2):
            send(s, ''.encode('utf-8'))
        else:    
            send(s, line.encode('utf-8'))
        
        while True:
            prefix = receive(s, 256) # username and directory prefix
            if bytes_to_int(prefix) == 2:
                output = receive(s, 1024)
                print(output.decode('utf-8'), end='', flush=True)
            else:
                print(prefix.decode('utf-8'), end='', flush=True)
                break


main()



