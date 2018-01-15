# Jason Van Kerkhoven
# 14/01/2018

# generic imports
import socket
import sys
import time

# declaring constants
PORT = 4907
BUFFER = 1024




#ping destination on PORT
def send(dest):
    # init socket
    i = 0;
    scope_id = socket.if_nametoindex('lowpan0') #socket.AF_INET6
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # send packets
    try:
        while(True):
            payload = 'echo ' + str(i)
            sock.sendto(payload.encode('utf-8'), (dest, PORT, 0, scope_id))
            print(payload)
            i += 1
            time.sleep(1)
    finally:
        sock.close()



#receiev pings on PORT
def receive():
    # init socket
    scope_id = socket.if_nametoindex('lowpan0') #socket.AF_INET6
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind(('', PORT, 0, scope_id))

    # receieve and print packets
    try:
        while(True):
            data, src = sock.recvfrom(BUFFER)
            print ('Receieved', '"'+data.decode('utf-8')+'"', 'from', src[0])
    finally:
        sock.close()
