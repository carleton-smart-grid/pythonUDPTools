import socket
import sys


SOCKET_TIMEOUT = 2 #socket timeout waiting for ack in seconds
SOCKET_RCV_BUFSIZE = 100 #socket buffer size for ack packet


def sendPacketUntilAck(ipv6Address, port, msg):
	successFlag = False
	sock.bind(('0.0.0.0', port))
	while (successFlag == False):
		sock.sendto(msg, (ipv6Address, port)) #send the packet 
		try:
			ackMsg, incomingaddr = sock.recvfrom(SOCKET_RCV_BUFSIZE)
			if (True): #if message is a valid ack - assume it is for now
				successFlag = True
		except socket.timeout:
			print 'socket timed out, retransmitting' #do nothing and let the while loop take care of retransmit


if len(sys.argv) < 3: #[self], ip address and port
	print 'Usage: python udpsender.py IP_ADDRESS PORT'
	sys.exit(0)

#sys.argv is at least 2 long
outgoingIp = sys.argv[1]
outgoingPort = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(SOCKET_TIMEOUT)

msg = 'Hello internet'
sendPacketUntilAck(outgoingIp, int(outgoingPort), msg)