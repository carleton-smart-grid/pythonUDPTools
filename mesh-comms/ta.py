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
DEFAULT_DB_PATH = 'dat/power-usages.db'



###############################################################################
# DECLARING FUNCTIONS
###############################################################################

# save xml data to database
def write(xml, curser, connection):
    #open XML file and get timestamp
    root = et.fromstring(xml)
    timestamp = root.find('./time').text

    #save info to db
    load = root.find('./currentload').text
    houseID = root.find('./homeid').text

    #parse date-time into correct format TODO use regular expression matching instead
    dateTime = timestamp.split(' ')
    dmy = dateTime[0].split('-')
    dateFormated = YEAR_CONSTANT + dmy[2] + '-' + dmy[1] + '-' + dmy[0]

    #insert to db
    insert = "INSERT INTO usages values(date('" + dateFormated + "'),time('" + dateTime[1] + "')," + houseID + "," + load + ")"
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

# receive-unpack-write loop
while(True):
    # receive and unpack data
    data = server.receive()
    data = packer.unpack(data)

    #save to SQLite3 server
    write(data, curser, connection)
