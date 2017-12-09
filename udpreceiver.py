import socket
import sys
import logging
import logging.handlers


# SOCKET_TIMEOUT = 5   # socket timeout unset
SOCKET_RCV_BUFSIZE = 4096   # Will set appropriately with size of 6LoWPAN packet


def verifyPacket(recvMsg):
	if (True):
	    logger.info('Received a packet, sending ack')
	    return True
	else:
	    logger.warning('Received an invalid packet, not acknowledging')
	    return False


def recvPacket(port):
	sock.bind(('', port, 0, socket.if_nametoindex('lowpan0')));
	recvMsg = sock.recv(4096) # Arbitrary (For now) buffer size



if len(sys.argv) < 2:  # [self], port
	print('Usage: python3 udpreceiver.py PORT')
	sys.exit(0)

# sys.argv is at least 2 long
incomingPort = sys.argv[1]

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
# sock.settimeout(SOCKET_TIMEOUT) # Currently no timeout.

logger = logging.getLogger('updReceiverLogger')
hdlr = logging.handlers.RotatingFileHandler('/var/log/udpReceiver.log')
hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Starting up')
# logger.setLevel() - don't do this for now, we want to log everything


while(True):
	recvPacket(incomingPort)
