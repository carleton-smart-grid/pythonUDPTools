# imports
import socket
import time
import sys

# called as client.py ADDRESS PORT
scope_id = socket.if_nametoindex('lowpan0')
while True:
    # socket setup
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    sock.connect((sys.argv[1], int(sys.argv[2]), 0, scope_id))

    # get data and dump
    data = sock.recv(1024)
    print(data.decode('utf-8'))

    # lather rinse and repeat
    time.sleep(5)
