# Jason Van Kerkhoven
# 05/01/2018



# import external libraries
import signal
import xml.etree.ElementTree as et
import sqlite3
import sys
# import exception

# import local py
import tcpcomms
import packer
import encryptiontool

# declaring constants
YEAR_CONSTANT = '20'
RSA_PACKET = 256
VALID_PACKET = 16
DEFAULT_DB_PATH = 'dat/power-usages.db'
DEADLOCK_TIMEOUT = 30 # 30 seconds of deadlock is generally locked enoug hthat there's no recovering

###############################################################################
# GRACEFUL SIGNAL HANDLING
###############################################################################
class Killer: 
    die = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGQUIT, self.quit)

    def terminate(self, signum, frame):
        printv("Terminate caught " + str(signum))
        self.die = True;
        raise InterruptedError

    def quit(self, signum, frame):
        printv("Quit caught " + str(signum))
        raise InterruptedError


###############################################################################
# DECLARING FUNCTIONS
###############################################################################
def timeoutSocket():
    printv("Socket deadlock detected - breaking lock")
    raise InterruptedError


def printv(string):
    if verbose:
        print(string)

# save xml data to database
def write(xml, curser, connection):
    # open XML file and get timestamp
    root = et.fromstring(xml)
    timestamp = root.find('./time').text

    # parse info out
    houseID = root.find('./homeid').text
    load = root.find('./currentload').text
    forecast = root.find('forecastload').text
    negociate = '1' if root.find('negociate').text.lower() in ('yes', 'true', 'enabled') else '0'
    negociateLoad = root.find('negociateload').text
    greenEnergy = root.find('greenenergy').text

    # parse date-time into correct format TODO use regular expression matching instead
    dateTime = timestamp.split(' ')
    dmy = dateTime[0].split('-')
    dateFormated = YEAR_CONSTANT + dmy[2] + '-' + dmy[1] + '-' + dmy[0]

    # generate sql and isert int database
    insert = ("INSERT INTO usages values("
              "DATE('" + dateFormated + "'), "
              "TIME('" + dateTime[1] + "'), "
              "" + houseID + ", "
              "" + load + ", "
              "" + forecast + ", "
              "" + negociate + ", "
              "" + negociateLoad + ", "
              "" + greenEnergy + ")")
    print(insert)
    curser.execute(insert)
    connection.commit()



###############################################################################
# PROGRAM START
###############################################################################

# initialize parameters to default
dbPath = DEFAULT_DB_PATH
encryptOn = False
verbose = False
killer = Killer()

# check for flags
flags = sys.argv
while (len(flags) > 0):
    flag = flags.pop(0)

    # database path flag
    if (flag == '-d'):
        dbPath = str(flags.pop(0))
    elif (flag == '-e'):
        encryptOn = True
    elif (flag == '-v'):
        verbose = True

# setup server object
server = tcpcomms.Server()

# setup db connection
connection = sqlite3.connect(dbPath)
curser = connection.cursor()

#instantiate security tool object
if(encryptOn):
    tool = encryptiontool.SecurityTool()


# receive-unpack-write loop
while(killer.die != True):

    socketDeadlockDetector = Timer(DEADLOCK_TIMEOUT, timeoutSocket) # We have to recreate this every time, we can't restart the same timer even though it's dead.
    socketDeadlockDetector.start() # Start the timer now - if DEADLOCK_TIMEOUT is hit, the server.receive function is locked and it will be interrupted

    # receive and unpack data
    try:
        packet = server.receive()
    except InterruptedError:
        print("Interrupted socket receive, continuing") # This is an error and as such is printed regardless of verbosity
        continue

    socketDeadlockDetector.cancel() # We've hit the end, cancel the timer regardless of how we got here, it will be restarted next time around

    #if the packet is an RSA encrypted AES key
    if(len(packet[0]) == RSA_PACKET and encryptOn):
        tool.addAesKey(packet)
    elif(len(packet[0]) == VALID_PACKET and encryptOn):
        #decrypt the data and attempt to unpack it
        data = tool.decryptAESData(packet)
    #No security, simply discard the IP information of the packet veriable
    else:
        data = packet[0]
    try:
        data = packer.unpack(data)
    except Exception as err:
        print('IMF unpack error: ', err)  # This is an error and as such is printed regardless of verbosity
        continue

    #save to SQLite3 server
    write(data, curser, connection)


# Cleanup - any future cleanup can go here.
del(server) # This doesn't necessarily have to be done, but it doesn't hurt.
print("Exiting")