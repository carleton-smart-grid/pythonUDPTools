import socket
import sys
import time
from subprocess import Popen, PIPE, STDOUT

# declaring constants
PORT = 34217
DEST_IP = "127.0.0.1" #Replace with correct IP
LOWPAN_IP = "dead:beef::1" #hardcoded because getting this in python is an absolute pain
BUFFER = 1024




#ping destination on PORT
def send(data, dest):
    # init socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send packets
    try:
        sock.sendto(data.encode('utf-8'), (dest, PORT))
        print(data)
    finally:
        sock.close()


def main():
    # p = Popen(["subl cliRPL.py", "show-parent"], shell=True, stdout=PIPE, stderr=PIPE)
    p = Popen(["ls | head", "-n", "1"], shell=True, stdout=PIPE, stderr=PIPE)
    parentOutput, stderr = p.communicate()
    print(parentOutput)
    # p = Popen(["sudo cliRPL.py", "show-current-dodag"], shell=True, stdout=PIPE, stderr=PIPE)
    p = Popen(["ls | tail", "-n", "1"], shell=True, stdout=PIPE, stderr=PIPE)
    dodagOutput, stderr = p.communicate()
    print(dodagOutput)
    #do processing of the data

    data = "child1,1024,root,256\n"

    send(data, DEST_IP)


if __name__ == "__main__":
    main()