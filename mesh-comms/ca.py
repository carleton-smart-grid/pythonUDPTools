# Nathaniel Charlebois
# 20/1/2018
#

# Importing libraries
import tcpcomms
import random
import packer
import sys

# Scheduling elements
# Attempted to use without success APscheduler
# Twisted (Reactor Pattern) seems like a reasonable alternative
# The current implemenation uses sleep() with drift correction
import time

# Declaring default flag values
verbose = False
transPeriod = 15*60
retrans = 5
pack = False

stack = []

# Declaring Constants
TA_IP = 'dead:beef::1'


# Defining Functions
# -----------------------------------------------------------------------------
def printv(string):
    if verbose:
        print(string)

#TODO Spoof data with time incrementation and realistic loads
def getData():
    xml = ( '<usagedata><homeid>15</homeid><time>01-01-15 15:00</time>'
            '<currentload>1.608475556</currentload>'
            '<forecastload>2.5</forecastload><negociate>Yes</negociate>'
            '<negociateload>7</negociateload>'
            '<greenenergy>1</greenenergy></usagedata>'
          )
    return xml;

def transmit(data):
    # TCP retransmission
    for attempt in range(0,retrans):
        try:
            printv(attempt)
            tcpcomms.send(TA_IP, data)

            # Returns if TCP is successful
            return True
            break
        except Exception as e:
            #TODO Handle varied errors e.g. (No route, Socket timeout, ect.)
            print(e)

    # Occurs given TCP transmission failure
    stack.append(data)
    return False

# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Handle user input from CLI
    flags = sys.argv
    print(flags)
    del flags[0]
    print(flags)
    while (len(flags) > 0):
        flag = flags.pop(0)
        # Verbose flag
        if flag == '-v':
            verbose = True
        # Set transmission period
        elif flag == '-t':
            transPeriod = int(flags.pop(0))*60 #convert to seconds
        # Set the number of retranmissions
        elif flag == '-r':
            retrans = int(flags.pop(0))
        # Set compression flag
        elif flag == '-c':
            pack = True

    # Main Loop logic
    while True:
        startTime = time.time()
        data = getData()

        # XML -> IMF
        if(pack):
            data = packer.pack(data)

        # Transmits the data and empties the stack
        if transmit(data) and stack:
            for item in stack:
                transmit(stack.pop())

        # Sleep the process for the transmission period
        # Corrects clock drift due to execution and retransmission time
        time.sleep(transPeriod - ((time.time() - startTime)% transPeriod))
