# Jason Van Kerkhoven
# 05/01/2018



# import external libraries
import xml.etree.ElementTree as et
import sqlite3
import sys

# import local py
import tcpcomms
import packer

# declaring constants
YEAR_CONSTANT = '20'
RSA_PACKET = 256
VALID_PACKET = 16
DEFAULT_DB_PATH = 'dat/power-usages.db'



###############################################################################
# DECLARING FUNCTIONS
###############################################################################

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

# check for flags
flags = sys.argv
while (len(flags) > 0):
    flag = flags.pop(0)

    # database path flag
    if (flag == '-d'):
        dbPath = str(flags.pop(0))

# setup server object
server = tcpcomms.Server()

# setup db connection
connection = sqlite3.connect(dbPath)
curser = connection.cursor()

#instantiate security tool object
tool = securityTools.SecurityTool()

# receive-unpack-write loop
while(True):
    # receive and unpack data
    packet = server.receive()
    #if the packet is an RSA encrypted AES key
    if(len(packet[0]) == RSA_PACKET)):
        tool.addAesKey(packet)
    elif(len(packet[0]) == VALID_PACKET):
        #decrypt the data and attempt to unpack it
        data = tool.decryptAESData(packet)
        try:
            data = packer.unpack(data)
        except Exception as err:
            print('IMF unpack error: ', err)
            continue

        #save to SQLite3 server
        write(data, curser, connection)
