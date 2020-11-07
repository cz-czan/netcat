import sys
import socket
import getopt
import subprocess

debug = True
bind_ip = ""
bind_port = 0

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def receive(socket, max_data_size):
    while True:
        data = socket.recv(max_data_size)
        #print("Data received. Responding with datasize.")
        socket.send(int_to_bytes(sys.getsizeof(data)))
        if(socket.recv(1) == True.to_bytes(1,'big')):
            #print("Datasize is correct. Data received successfully.")
            return data
        else:
            #print("Datasize incorrect. Retrying data transfer.")
            continue


def send(socket, data: bytes):
    while True:
        socket.send(data)
        #print("Data sent.")
        r_datasize = bytes_to_int(socket.recv(64))
        if(r_datasize == sys.getsizeof(data)):
            socket.send(True.to_bytes(1,'big'))
            #print("Received datasize corresponds to local datasize. Data sent successfully.")
            return
        else:
            socket.send(bytes(1)) # (negative bit)
            #print("Received size:" + r_datasize + " Local size:" + sys.getsizeof(data))
            #print("Incorrect datasize received. Retrying data transfer.")
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
send(client, "<#CMD:>".encode('utf-8'))
def main():
    print("waiting for client input")
    client_buffer = receive(client, 512)
    print("client input received")
    print(client_buffer)
    print("<#client:>" + client_buffer.decode('utf-8'), end='')

    process = subprocess.Popen(client_buffer.decode('utf-8').split(), stdout = subprocess.PIPE) # Creating a process
    #print("PROCESS CREATED") # debug
    while True: # Reading and sending the stdout from the process in realtime
        shell_output = process.stdout.readline() # Read a line from stdout
        return_code = process.poll()
        print(shell_output)
        print(return_code)
        if shell_output.decode('utf-8') == '' and return_code is not None: 
            #print("Process execution complete. Sending netcat shell prefix")
            send(client, "<#CMD:>".encode('utf-8'))
            break
        elif shell_output: 
            #print("Process execution incomplete.")
            send(client, int_to_bytes(2)) 
            #print("Response code 2 sent to client")
            send(client, shell_output)
            #print("Shell output sent to client")
            while True: 
                response =  receive(client, 16)
                if (bytes_to_int(response) != 1):
                    send(client, shell_output) 
                    #print("RESENDING DATA")
                else:
                    break


            
while True:
	main()
