import sys
import getpass
import os


class color:
    user = "\033[92m"
    dir = "\033[94m"
    endc = "\033[0m"



def cwd(): # Replaces user home dir with ~
    if(os.getcwd().startswith("/home/" + getpass.getuser())):
        return "~" + os.getcwd()[len("/home/" + getpass.getuser()):]
    else:
        return os.getcwd()

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bytes_to_int(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

# receive() and send() ensure successful data transfer and fixes synchronisation issues
def receive(socket, max_data_size):
    while True:
        data = socket.recv(max_data_size)
        # Data received. Responding with datasize.
        socket.send(int_to_bytes(sys.getsizeof(data)))
        if socket.recv(1) == True.to_bytes(1, 'big'):
            # Datasize is correct. Data received successfully.
            return data
        else:
            # Datasize incorrect. Retrying data transfer.
            continue

def send(socket, data: bytes):
    while True:
        socket.send(data)
        # print("Data sent.")
        r_datasize = bytes_to_int(socket.recv(64))
        if r_datasize == sys.getsizeof(data):
            socket.send(True.to_bytes(1, 'big'))
            # print("Received datasize corresponds to local datasize. Data sent successfully.")
            return
        else:
            socket.send(bytes(1))  # (negative bit)
            # print("Received size:" + r_datasize + " Local size:" + sys.getsizeof(data))
            # print("Incorrect datasize received. Retrying data transfer.")
