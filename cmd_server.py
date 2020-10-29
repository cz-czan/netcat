import sys
import socket
import getopt
import subprocess

bind_ip = ""
bind_port = 0

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["target", "port"])

    for o, a in opts:
        if o in ("-t", "--target"):
        	bind_ip = a
        elif o in ("-p", "--port"):
        	bind_port = a
except getopt.GetoptError as err:
	print(str(err))

bind_full_addr = socket.getaddrinfo(bind_ip, bind_port)[0][4]

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind(bind_full_addr)
server.listen(5)
print("waiting for connection...")
client, addr = server.accept()


def run(command):
    try:
        o = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return o #encoded in utf-8
    except Exception as err:
        return str(err).encode('utf-8')
    
def main():
    client.send("<#CMD:>".encode('utf-8'))
    client_buffer = client.recv(512)
    print("<#client:>" + client_buffer.decode('utf-8'), end='')
    cmd_output = run(client_buffer.decode('utf-8'))
    print(cmd_output.decode('utf-8'))
    client.send(cmd_output)
client.send("<#CMD:>".encode('utf-8'))
while True:
	main()
