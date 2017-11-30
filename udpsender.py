import socket
import sys
import logging
import logging.handlers


SOCKET_TIMEOUT = 5   # socket timeout waiting for ack in seconds
SOCKET_RCV_BUFSIZE = 100   # socket buffer size for ack packet


def verifyAck(ackMsg):
    if (True):
        logger.info('Received a valid ack')
        return True
    else:
        logger.warning('Received an invalid ack')
        return False


def sendPacketUntilAck(ipv6Address, port, msg):
    sock.bind(('0.0.0.0', port))
    while (True):
        sock.sendto(msg, (ipv6Address, port))  # send the packet
        logmsg = 'Sending packet : ' + msg.decode()
        logger.info(logmsg)
        try:
            ackMsg, incomingaddr = sock.recvfrom(SOCKET_RCV_BUFSIZE)
            if (verifyAck(ackMsg)):  # if message is a valid ack - verifyack takes care of logging
                break
        except socket.timeout:
            logger.warning('Socket timed out, retransmitting')  # do nothing and let the while loop take care of retransmit


if len(sys.argv) < 3:  # [self], ip address and port
    print('Usage: python udpsender.py IP_ADDRESS PORT')
    sys.exit(0)

# sys.argv is at least 2 long
outgoingIp = sys.argv[1]
outgoingPort = sys.argv[2]

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.settimeout(SOCKET_TIMEOUT)

logger = logging.getLogger('updSenderLogger')
hdlr = logging.handlers.RotatingFileHandler('/var/log/udpSender.log')
hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Starting up')
# logger.setLevel() - don't do this for now, we want to log everything


while(True):
    msg = input(">> ")
    sendPacketUntilAck(outgoingIp, int(outgoingPort), msg.encode())
