import socket
import getopt
import subprocess
from utils import *
import getpass
import sys

debug = True
bind_ip = ""
bind_port = 0
ipv6 = False

command = False
upload = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "t:p:i:", ["target", "port", "ip"])

    for o, a in opts:
        if o in ("-t", "--target"):
            bind_ip = a
        elif o in ("-p", "--port"):
            bind_port = a
        elif o in ("-i","--ip"):
            if a == "6":
                ipv6 = True
            elif a == "4":
                ipv6 = False
            else:
                sys.exit('Provide a proper IP Protocol for the server to operate on in the -i option (usage: -i 6 / -i 4 )')


except getopt.GetoptError as err:
    print(str(err))
server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
if ipv6:
    bind_full_addr = socket.getaddrinfo(bind_ip, bind_port)[0][4]
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.bind(bind_full_addr)
    server.listen(5)
    print("Awaiting connection...")
    client, addr = server.accept()
    print("Connection established with " + addr[0] + " over IPv6")
else:
    bind_full_addr = socket.getaddrinfo(bind_ip, bind_port)[1][4]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(bind_full_addr)
    server.listen(5)
    print("Awaiting connection...")
    client, addr = server.accept()
    print("Connection established with " + addr[0] + " over IPv4")

c_opts = receive(client, 1024).decode("utf-8")
if "u" in c_opts:
    filename = receive(client, 256).decode('utf-8')
    data = receive(client, 16384)
    file = open(filename, "wb")
    file.write(data)
    file.close()
    print("File transfer successful")
    client.close()
    sys.exit()

send(client, ("<#" + color.user + getpass.getuser() + color.endc + "@" + color.dir + cwd() + color.endc + ">").encode('utf-8'))

def execute(client_buffer):
    if client_buffer.decode('utf-8').startswith('cd '):
        try:
            os.chdir(client_buffer.split()[1])
            send(client, ("<#" + color.user + getpass.getuser() + color.endc + "@" + color.dir + cwd() + color.endc + ">").encode('utf-8'))
        except Exception as e:
            shell_output = str(e) + "\n" # Read a line from stdout
            return_code = 0
            print(shell_output)
            print(return_code)
            send(client, int_to_bytes(2)) 
            send(client, shell_output.encode('utf-8'))
            while True: 
                response =  receive(client, 16)
                if (bytes_to_int(response) != 1):
                    send(client, shell_output.encode('utf-8'))
                else:
                    break

            send(client, ("<#" + color.user + getpass.getuser() + color.endc + "@" + color.dir + cwd() + color.endc + ">").encode('utf-8'))
    else:
        try:
            process = subprocess.Popen(client_buffer.decode('utf-8').split(), stdout = subprocess.PIPE) # Creating a process
            while True: # Reading and sending the stdout from the process in realtime
                shell_output = process.stdout.readline() # Read a line from stdout
                return_code = process.poll()
                print(shell_output)
                print(return_code)
                if shell_output.decode('utf-8') == '' and return_code is not None: 
                    # Process execution complete. Sending user prefix
                    send(client, ("<#" + color.user + getpass.getuser() + color.endc + "@" + color.dir + cwd() + color.endc + ">").encode('utf-8'))
                    break
                elif shell_output: 
                    # Process execution incomplete, signaling to client with code 2
                    send(client, int_to_bytes(2))
                    # And sending the next line of stdout
                    send(client, shell_output)

        except Exception as e:
            shell_output = str(e) + "\n" # Read a line from stdout
            return_code = 0
            print(shell_output)
            print(return_code)
            send(client, int_to_bytes(2)) 
            send(client, shell_output.encode('utf-8'))
            #while True:
            #    response =  receive(client, 16)
            #    if (bytes_to_int(response) != 1):
            #        send(client, shell_output.encode('utf-8'))
            #        print("REFERENCE POINT")
            #    else:
            #        break

            send(client, ("<#" + color.user + getpass.getuser() + color.endc + "@" + color.dir + cwd() + color.endc + ">").encode('utf-8'))
    

def main():
    print("Awaiting client input")
    client_buffer = receive(client, 512)
    print("Client input received")
    print(client_buffer)
    print("<#client:>" + client_buffer.decode('utf-8'), end='')

    execute(client_buffer)



            
while True:
    main()
