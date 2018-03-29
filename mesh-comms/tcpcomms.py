# Jason Van Kerkhoven
# 30/12/2017

# generic imports
import socket
import sys

# declaring variables/constants
PORT = 4907
HOST = ''
BUFFER = 1024
TIMEOUT_SEC = 15
verbose = True


# what it says on the tin
def printv(s):
    if (verbose):
        print(s)


# send a data string to destination, given as string OR bytearray
# meant as a "one shot" transfer, socket setup/teardown internal
def send(dest, data):
    try:
        # socket setup
        printv('Establishing connection...')
        scope_id = socket.if_nametoindex('lowpan0')
        #scope_id = socket.AF_INET
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        sock.settimeout(TIMEOUT_SEC)
        sock.connect((dest, PORT, 0, scope_id))
        #sock.connect((dest, PORT))


        # send
        printv('Sending data...')
        if (isinstance(data, str)):
            data = data.encode()
        sock.send(data)
        printv('Data sent!')
    # catches all socket errors
    except socket.error:
        # Raises the timeout error to the ca.py scope
        raise
    finally:
        sock.close()
        printv('Socket closed!')


# Solve the little problem of variable scope on imports
# auto runs startup() on init, don't forget to teardown()
class Server:
    # declaring local instance variables
    serverSocket = None


    # generic constructor
    def __init__(self):
        printv('Server startup...')
        self.setup()
        serverSocket = None


    # generic destructor
    def __del__(self):
        printv('Server shutdown...')
        self.teardown()
        serverSocket = None


    # setup server socket for regular comms
    def setup(self):
        # socket setup
        printv('Binding Socket on port', PORT, '...')
        scope_id = socket.if_nametoindex('lowpan0')
        #scope_id = socket.AF_INET
        self.serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.serverSocket.bind((HOST, PORT, 0, scope_id))
        #self.serverSocket.bind((HOST, PORT))
        self.serverSocket.listen(1)
        printv('Socket bind complete!')


    # properly terminate server
    def teardown(self):
        if (self.serverSocket != None):
            print('Closing socket...')
            self.serverSocket.close


    # recieve data over multiple transactions
    # socket exists outside function scope, setup() before, teardown() after
    # returns 'bytearray' type of recieved data
    def receive(self):
        # wait for connection
        printv('Waiting for connection...')
        connection, src = self.serverSocket.accept()
        printv('Connection with:', src)

        # get all data
        data = bytearray()
        while (True):
            payload = connection.recv(BUFFER)
            if (not payload):
                break
            printv('Receieved', len(payload), 'Byte(s)...')
            data.extend(payload)

        # close current connection and returns a tuple with the data and IP address
        printv('Total:', len(data), 'Byte(s)')
        printv('Closing connection with:', src)
        connection.close()
        return (data, src[0])
