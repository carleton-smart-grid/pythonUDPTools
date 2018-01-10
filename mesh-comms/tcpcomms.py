# Jason Van Kerkhoven
# 30/12/2017

# generic imports
import socket
import sys
import logging
import logging.handlers

# declaring constants
PORT = 4907
HOST = ''
BUFFER = 1024
TIMEOUT_SEC = 15


#Logger setup - this is all global so that all functions and classes can use the logger.
#I can't figure out a better solution than that.
logger = logging.getLogger('tcpcommlog')
hdlr = logging.handlers.RotatingFileHandler('/var/log/tcpcomms.log')
hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#Set the logger level appropriately - acceptable is 20,30,40,50 or the logging constants logging.INFO,WARNING,ERROR,CRITICAL
def setLogLevel(loglevel):
    if (isinstance(loglevel, int)):
        logger.setLevel(loglevel)


# send a data string to destination, given as string OR bytearray
# meant as a "one shot" transfer, socket setup/teardown internal
def send(dest, data):
    try:
        # socket setup
        logger.info('Establishing connection...')
        scope_id = socket.AF_INET #socket.if_nametoindex('lowpan0')
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        sock.settimeout(TIMEOUT_SEC)
        sock.connect((dest, PORT, 0, scope_id))

        # send
        logger.info('Sending data...')
        if (isinstance(data, str)):
            data = data.encode()
        sock.send(data)
        logger.info('Data sent!')
    except socket.error:
        logger.warning('Error sending data from the socket')
    finally:
        sock.close()
        logger.info('Socket closed!')


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
        logger.info('Binding Socket on port', PORT, '...')
        scope_id = socket.AF_INET #socket.if_nametoindex('lowpan0')
        self.serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.serverSocket.bind((HOST, PORT, 0, scope_id))
        self.serverSocket.listen(1)
        logger.info('Socket bind complete!')


    # properly terminate server
    def teardown(self):
        if (self.serverSocket != None):
            logger.info('Closing socket...')
            self.serverSocket.close


    # recieve data over multiple transactions
    # socket exists outside function scope, setup() before, teardown() after
    # returns 'bytearray' type of recieved data
    def receive(self):
        # wait for connection
        logger.info('Waiting for connection...')
        connection, src = self.serverSocket.accept()
        logger.info('Connection with:', src)

        # get all data
        data = bytearray()
        while (True):
            payload = connection.recv(BUFFER)
            if (not payload):
                break
            logging.info('Receieved', len(payload), 'Byte(s)...')
            data.extend(payload)

        # close current connection and return
        logger.info('Total:', len(data), 'Byte(s)')
        logger.info('Closing connection with:', src)
        connection.close()
        return data
