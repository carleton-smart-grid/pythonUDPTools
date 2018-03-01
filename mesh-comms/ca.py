# Nathaniel Charlebois
# 20/1/2018
#

# Importing libraries
import tcpcomms
import random as rn
import packer
import sys
import collections
from datetime import datetime

# Scheduling elements
# Attempted to use without success APscheduler
# Twisted (Reactor Pattern) seems like a reasonable alternative
# The current implemenation uses sleep() with drift correction
import time

# Declaring default flag values
verbose = False
transPeriod = 15*60 #15 Minutes
retrans = 5
pack = False
homeId = 1

stack = []

# Declaring Constants
taIP = 'dead:beef::1'


# Defining Functions
# -----------------------------------------------------------------------------
def printv(string):
    if verbose:
        print(string)

def generateData():
    # Rand range defined in named tuples
    Limit = collections.namedtuple('Limit', 'lower upper')
    currentLoad = Limit(0,5)
    forecastLoad = Limit(0,5)

    # Formatting current time to match the provided H.E.M.S. XML
    timeStamp = datetime.now().strftime('%d-%m-%y %H:%M')

    # Build XML
    xml = '<usagedata><homeid>{}</homeid><time>{}</time>'.format(homeId,timeStamp)
    # PyFormat allows for the adjustment of float precision e.g. {:10.9f}
    # rn.uniform() returns an IEEE-754 53-bit float
    xml += '<currentload>{}</currentload>'.format(rn.uniform(currentLoad.lower,currentLoad.upper))
    xml += '<forecastload>{}</forecastload>'.format(rn.uniform(forecastLoad.lower,forecastLoad.upper))
    # The below fields are irrelevant so they remain static
    xml += '<negociate>Yes</negociate><negociateload>7</negociateload><greenenergy>1</greenenergy></usagedata>'
    return xml;

def transmit(data):
    # TCP retransmission
    for attempt in range(0,retrans):
        try:
            printv('Attempt {}'.format(attempt))
            tcpcomms.send(taIP, data)

            # Returns if TCP is successful
            return True
            break
        except Exception as e:
            #TODO Handle varied errors e.g. (No route, Socket timeout, ect.)
            print(e)

    # Occurs given TCP transmission failure
    printv('\nTransmission Failed!\nAppending data to the stack for future retranmission\n')
    stack.append(data)
    return False

# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Handle user input from CLI
    flags = sys.argv[1:]

    while (len(flags) > 0):
        flag = flags.pop(0)
        # Verbose flag
        if flag == '-v':
            verbose = True

        # Set transmission period
        elif flag == '-t':
            transPeriod = int(flags.pop(0))#*60 #convert to seconds

        # Set the number of retranmissions
        elif flag == '-r':
            retrans = int(flags.pop(0))

        # Set compression flag
        elif flag == '-c':
            pack = True

        elif flag == '-a':
            taIP = flags.pop(0)

        elif flag == '-h':
            homeId = int(flags.pop(0))

    printv('Details:')
    printv('\t{:30} {}'.format('TA IP address',taIP))
    printv('\t{:30} {}'.format('Home ID',homeId))
    printv('\t{:30} {} seconds'.format('Retransmission Period',transPeriod))
    printv('\t{:30} {}'.format('Retransmission attempts',retrans))
    printv('\t{:30} {}\n'.format('XML to IMF compression',pack))



    # Main Loop logic
    while True:
        startTime = time.time()
        data = generateData()

        # XML -> IMF
        if(pack):
            data = packer.pack(data)

        # Transmits the data and empties the stack
        if transmit(data) and stack:
            for item in stack:
                printv('Transmitting a previous entry from the stack...')
                transmit(stack.pop())

        # Sleep the process for the transmission period
        # Corrects clock drift due to execution and retransmission time
        # Utilizes Unix Epoch Time
        time.sleep(transPeriod - ((time.time() - startTime)% transPeriod))
