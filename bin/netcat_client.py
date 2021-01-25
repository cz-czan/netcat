import sys
import socket
import getopt
from utils import *

server_address = ""
server_port = 0
ipv6 = False

file_path = ""
c_opts = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "t:p:i:cu:", ["target", "port", "command", "upload"])

    for o, v in opts: # o - option; v - value
        if o in ("-t", "--target"):
            server_address = v
        elif o in ("-p", "--port"):
            server_port = int(v)
        elif o in ("-u", "--upload"):
            file_path = v
            c_opts += "u"
        elif o in ("-i","--ipv"):
            if v == "6":
                ipv6 = True
            elif v == "4":
                ipv6 = False
            else:
                sys.exit('Provide a proper IP Protocol for the client to operate on in the -i option (usage: -i 6 / -i 4 )')

except getopt.GetoptError as err:
    print(str(err))
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# You can not actually receive an empty string with socket.recv(), hence i add a random character for a quick fix.
# this should be fixed in the send()/receive() functions in utils.py
c_opts += "."
if ipv6:
    print("Creating TCP/IPv6 socket")
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    print("Connecting with " + str(server_address) + " on port " + str(server_port))
    print(s.connect((server_address, server_port)))
    print("Connection established")
    send(s, c_opts.encode('utf-8'))
else:
    print("Creating TCP/IPv4 socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting with " + str(server_address) + " on port " + str(server_port))
    print(s.connect((server_address, server_port)))
    print("Connection established")
    send(s, c_opts.encode('utf-8'))

if "u" in c_opts:
    file = open(file_path, "rb")
    data = file.read()

    # send filename
    send(s, os.path.basename(file_path).encode('utf-8'))
    # send file content
    send(s, data)

    s.close()
    sys.exit()

# Waiting for the commandline prefix ( 16 bytes max ) and printing
print(receive(s, 1024).decode('utf-8'), end='', flush=True)
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



