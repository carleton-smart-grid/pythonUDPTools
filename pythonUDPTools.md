# UDP sender

Usage:
`python udpsender.py IP_ADDRESS PORT`

The udp sender sends a packet (currently containing just 'hello internet' for testing) to the address and port specified and waits for a response for `SOCKET_TIMEOUT` seconds (defined in the script), if there is no response, it retransmits.

At the moment, the response is not parsed, and is assumed to be a valid ack packet.

