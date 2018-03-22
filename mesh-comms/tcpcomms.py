# Jason Van Kerkhoven
# 30/12/2017

# generic imports
import socket
import sys

# declaring constants
PORT = 4907
HOST = ''
BUFFER = 1024
TIMEOUT_SEC = 15


# send a data string to destination, given as string OR bytearray
# meant as a "one shot" transfer, socket setup/teardown internal
def send(dest, data):
    try:
        # socket setup
        print('Establishing connection...')
        scope_id = socket.if_nametoindex('lowpan0')
        #scope_id = socket.AF_INET
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        sock.settimeout(TIMEOUT_SEC)
        sock.connect((dest, PORT, 0, scope_id))
        #sock.connect((dest, PORT))


        # send
        print('Sending data...')
        if (isinstance(data, str)):
            data = data.encode()
        sock.send(data)
        print('Data sent!')
    # catches all socket errors
    except socket.error:
        # Raises the timeout error to the ca.py scope
        raise
    finally:
        sock.close()
        print('Socket closed!')


# Solve the little problem of variable scope on imports
# auto runs startup() on init, don't forget to teardown()
class Server:
    # declaring local instance variables
    serverSocket = None
    # generic constructor
    def __init__(self):
        print('Server startup...')
        self.setup()
        serverSocket = None


    # generic destructor
    def __del__(self):
        print('Server shutdown...')
        self.teardown()
        serverSocket = None


    # setup server socket for regular comms
    def setup(self):
        # socket setup
        print('Binding Socket on port', PORT, '...')
        scope_id = socket.if_nametoindex('lowpan0')
        # scope_id = socket.AF_INET
        self.serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.serverSocket.bind((HOST, PORT, 0, scope_id))
        #self.serverSocket.bind((HOST, PORT))
        self.serverSocket.listen(1)
        print('Socket bind complete!')


    # properly terminate server
    def teardown(self):
        if (self.serverSocket != None):
            print('Closing socket...')
            self.serverSocket.shutdown(socket.SHUT_RDWR) # Shutdown reads and writes


    # recieve data over multiple transactions
    # socket exists outside function scope, setup() before, teardown() after
    # returns 'bytearray' type of recieved data
    def receive(self):
        # wait for connection
        print('Waiting for connection...')
        connection, src = self.serverSocket.accept()
        print('Connection with:', src)

        # get all data
        data = bytearray()
        while (True):
            payload = connection.recv(BUFFER)
            if (not payload):
                break
            print('Receieved', len(payload), 'Byte(s)...')
            data.extend(payload)

        # close current connection and returns a tuple with the data and IP address
        print('Total:', len(data), 'Byte(s)')
        print('Closing connection with:', src)
        connection.close()
        return (data, src[0])
