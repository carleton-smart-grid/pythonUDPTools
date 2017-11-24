# generic imports
import socket
import sys

# magic python pseudocode for accept anything
HOST = ''

# called used server.py PORT
# socket setup
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
scope_id = socket.if_nametoindex('lowpan0')
sock.bind((HOST, int(sys.argv[1]), 0, scope_id))
sock.listen(1)

# send loop
while True:
    conn, addr = sock.accept()
    print('connected!')
    print('sending "hello world"...')
    conn.send('hello world')
    conn.close()
    print('closing connecting...')
