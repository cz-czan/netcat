import sys
import socket
import getopt

server_address = ""
server_port = 0

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
print(receive(s, 16).decode('utf-8'), end='', flush=True) # Waiting for the console prefix ( 16 bytes max ) and printing
def main():
    for n, line in enumerate(sys.stdin):
        if(len(line) < 2):
            send(s, ''.encode('utf-8'))
        else:    
            send(s, line.encode('utf-8'))
        
        while True:
            prefix = receive(s, 16)
            if bytes_to_int(prefix) == 2:
                output = receive(s, 1024)
                #print("Output data received.")
                print(output.decode('utf-8'), end='', flush=True)
                send(s, int_to_bytes(1)) # Data receival confirmation
                #print("confirming...")
            else:
                print(prefix.decode('utf-8'), end='', flush=True)
                break


main()



