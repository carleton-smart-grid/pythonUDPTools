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
    except socket.error:
        print("No network, not sending")
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

    while(True):
	    p = Popen(["sudo cliRPL.py show-dao-parent"], shell=True, stdout=PIPE, stderr=PIPE)
	    parentOutput, stderr = p.communicate()
	    # print(parentOutput)
	    parentRank = re.search(r'.*rank: (\d+).*', parentOutput)
	    if (parentRank is not None):
	        parentRank = parentRank.group(1)
	    else:
	        parentRank = None

	    # print(parentRank)
	    parentIPSuffix = re.search(r'address: fe80::([\da-f:]*)$',parentOutput, flags=re.MULTILINE)
	    if (parentIPSuffix is not None):
	        parentIPSuffix = parentIPSuffix.group(1)
	    else :
	        parentIPSuffix = None

	    # print(parentIPSuffix)
	    p = Popen(["sudo cliRPL.py show-current-dodag"], shell=True, stdout=PIPE, stderr=PIPE)
	    dodagOutput, stderr = p.communicate()
	    myRank = re.search(r'Rank: (\d+)', dodagOutput).group(1)
	    #do processing of the data

	    data = lowpanIP + "," + myRank
	    if ((parentIPSuffix is not None) and (parentRank is not None)):
	        data += "," + parentIPSuffix + "," + parentRank



	    send(data, destIP)

	    time.sleep(1)


if __name__ == "__main__":
    main()
