import sys
import socket
import getopt
import subprocess

bind_ip = ""
bind_port = 0

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

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
client.send("<#CMD:>".encode('utf-8'))
def main():
    #client.send("<#CMD:>".encode('utf-8'))
    print("waiting for client input")
    client_buffer = client.recv(512)
    print("client input received")
    print(client_buffer)
    print("<#client:>" + client_buffer.decode('utf-8'), end='')

    process = subprocess.Popen(client_buffer.decode('utf-8').split(), stdout = subprocess.PIPE) # Creating a process
    print("PROCESS CREATED") # debug
    while True: # Reading and sending the stdout from the process in realtime
        shell_output = process.stdout.readline() # Read a line from stdout
        return_code = process.poll()
        print(shell_output)
        print(return_code)
        if shell_output.decode('utf-8') == '' and return_code is not None: 
            print("Process execution complete. Sending netcat shell prefix")
            client.send("<#CMD:>".encode('utf-8'))
            break
        elif shell_output: 
            print("Process execution incomplete.")
            client.send(int_to_bytes(2)) 
            print("Response code 2 sent to client")
            client.send(shell_output)
            print("Shell output sent to client")
            while True: 
                response =  client.recv(16)
                if (bytes_to_int(response) != 1):
                    client.send(shell_output) 
                    print("RESENDING DATA")
                else:
                    break


            
while True:
	main()
