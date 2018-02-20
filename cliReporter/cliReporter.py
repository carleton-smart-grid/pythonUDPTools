import socket
import sys
import time
from subprocess import Popen, PIPE, STDOUT
import re

# declaring constants
PORT = 34217
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
    # check arguments
    if (len(sys.argv) != 3):
        print('ERROR: Unexpected argument amount - 2 expected')
        print('       Please call with arguments: SELF_IPv6 DEST_IPv4')
        sys.exit()

    # save arguments
    lowpanIP = sys.argv[1]
    destIP = sys.argv[2]

    p = Popen(["subl cliRPL.py", "show-parent"], shell=True, stdout=PIPE, stderr=PIPE)
    # p = Popen(["ls | head", "-n", "1"], shell=True, stdout=PIPE, stderr=PIPE)
    parentOutput, stderr = p.communicate()
    parentRank = re.match("rank: (\d+)", parentOutput)
    print(parentRank.group(1))
    # p = Popen(["sudo cliRPL.py", "show-current-dodag"], shell=True, stdout=PIPE, stderr=PIPE)
    p = Popen(["ls | tail", "-n", "1"], shell=True, stdout=PIPE, stderr=PIPE)
    dodagOutput, stderr = p.communicate()
    print(dodagOutput)
    #do processing of the data

    data = "child1,1024,root,256\n"

    send(data, destIP)


if __name__ == "__main__":
    main()
