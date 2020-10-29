import sys
import socket
import getopt

server_address = ""
server_port = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"t:p:",["target","port"])

    for o,a in opts:
        if o in ("-t","--target"):
            server_address = a
        if o in ("-p", "--port"):
            server_port = int(a)
except getopt.GetoptError as err:
    print(str(err))

print("target: " + server_address + " | port: " + str(server_port))

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) #creating a tcp-ipv6 socket
s.connect((server_address, server_port))

print("connection established with: " + server_address + " on port: " + str(server_port))

print(s.recv(16).decode('utf-8'), end='', flush=True)
for n, line in enumerate(sys.stdin):
    prefix = s.recv(16)
    print(prefix.decode('utf-8'), end='', flush=True)
    s.send(line.encode('utf-8'))
    response = s.recv(1024).decode('utf-8')
    print(response)

