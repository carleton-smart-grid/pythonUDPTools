# Jason Van Kerkhoven
# 04/01/2018

# import external libraries
import xml.etree.ElementTree as et
import struct
import re
import time
from datetime import datetime as dt

# declaring constants
YEAR_CONSTANT = '20'




# convert float to 4B bytearray (LSB at 0)
# RETURNS bytearray, length 4
def floatToBytes(num):
    return bytearray(struct.pack('f', num))


# convert 4 byte bytearray into float (LSB at 0)
# RETURNS float
def bytesToFloat(bytes):
    return float(struct.unpack('f', bytes)[0])

# convert int to bitstring
# RETURNS string equal to num as binary, will be 0 padded if length is less than minLength parameter
def intToBits(num, minLength):
    bits = '{0:b}'.format(num)
    while (len(bits) < minLength):
        bits = '0' + bits
    return bits


# convert bytes or bytearray to int, (LSB at 0)
# RETURNS int
def bytesToInt(bytes):
    r = 0
    for b in reversed(bytes):
        r = r*256 + int(b)
    return r


# get bytearray as string of bytes
# RETURNS string
def printableByteArray(arr):
    return str([ "0x%02x" % byte for byte in arr ])


# pack data from XML
# RETURNS a bytearray in IMF format
def pack(xmlContents):
    # init xml root element and imf returnable
    root = et.fromstring(xmlContents)
    imf = bytearray()

    # parse homeid, default 0
    homeid = root.find('./homeid')
    if (homeid != None):
        homeid = int(homeid.text) if homeid.text != None else 0
        if (homeid > 255 or homeid < 0):
            homeid = 0
    else:
        homeid = 0
    # add homid to imf
    imf.extend((homeid,))

    # parse time, default 0
    unixstamp = (0x00,0x00,0x00,0x00)
    timestamp = root.find('./time')
    # check validity
    if (timestamp != None):
        timestamp = timestamp.text
        if (timestamp != None):
            if (re.match('(\d+-\d+-\d+)\s+(\d+:\d+)', timestamp)):
                #convert to unix stamp
                dateTime = timestamp.split(' ')
                dmy = dateTime[0].split('-')
                dateFormated = YEAR_CONSTANT + dmy[2] + '-' + dmy[1] + '-' + dmy[0]
                unixstamp = int(time.mktime(time.strptime(dateFormated+' '+dateTime[1], '%Y-%m-%d %H:%M')))
                unixstamp = unixstamp.to_bytes(4, byteorder='little')

    # add time to imf TODO actually convert to UNIX stamp
    imf.extend(unixstamp)

    # parse current load, default 0
    currentload = root.find('./currentload')
    if (currentload != None):
        currentload = float(currentload.text) if currentload.text != None else 0.0
    else:
        currentload = 0.0
    # add currentload
    imf.extend(floatToBytes(currentload))

    # parse forecast load, default 0
    forecastload = root.find('./forecastload')
    if (forecastload != None):
        forecastload = float(forecastload.text) if forecastload.text != None else 0.0
    else:
        forecastload = 0.0
    # add forecastload
    imf.extend(floatToBytes(forecastload))

    # parse negociate, default False
    negociate = root.find('./negociate')
    if (negociate != None):
        negociate = negociate.text.lower() in ('yes','true','enabled')
    else:
        negociate = False
    # parse negociateload, default 0
    negociateload = root.find('./negociateload')
    if (negociateload != None):
        negociateload = int(negociateload.text) if negociateload.text != None else 0
        if (negociateload > 7):
            negociateload = 7
        elif (negociateload < 0):
            negociateload = 0
    else:
        negociateload = 0
    # parse greenenergy, default 0
    greenenergy = root.find('./greenenergy')
    if (greenenergy != None):
        greenenergy = int(greenenergy.text) if greenenergy.text != None else 0
        if (greenenergy > 15):
            greenenergy = 15
        elif (greenenergy < 0):
            greenenergy = 0
    else:
        greenenergy = 0
    #add all 3 above attributes into bytearray
    byte = ''
    if (negociate):
        byte += '1'
    else:
        byte += '0'
    byte += intToBits(negociateload, 3)
    byte += intToBits(greenenergy, 4)
    imf.extend((int('0b'+byte, 2),))

    return imf



# unpack data into XML
# RETURNS a XML-esque UTF-8 character string
def unpack(packetContents):
    #start xml
    xml = '<usagedata>'

    # extract homeid
    homeid = int(packetContents[0])
    # update xml attribute
    xml += '<homeid>' + str(homeid) + '</homeid>'

    # extract unix timestamp
    unixstamp = bytesToInt(packetContents[1:5])
    timestamp = (dt.fromtimestamp(unixstamp)).strftime('%d-%m-%y %H:%M')
    # update xml attribute
    xml += '<time>' + str(timestamp) + '</time>'

    # extract currentload
    currentload = bytesToFloat(packetContents[5:9])
    # update xml attribute
    xml += '<currentload>' + str(currentload) + '</currentload>'

    # extract forecastload
    forecastload = bytesToFloat(packetContents[9:13])
    # update xml attribute
    xml += '<forecastload>' + str(forecastload) + '</forecastload>'

    # extract negociate
    b = packetContents[13]
    negociate = 'Yes' if (((b & 0x80) >> 7) == 1) else 'No'
    # extract negociateload
    negociateload = (b & 0x70) >> 4
    # extract greenenergy
    greenenergy = (b & 0x0F)
    # update xml attributes
    xml += '<negociate>' + str(negociate) + '</negociate>'
    xml += '<negociateload>' + str(negociateload) + '</negociateload>'
    xml += '<greenenergy>' + str(greenenergy) + '</greenenergy>'

    # terminate root and return
    return str(xml + '</usagedata>')




# debug
'''
##########################################################################
print('starting...\n')
xml = '<usagedata><homeid>15</homeid><time>01-01-15 15:00</time><currentload>1.608475556</currentload><forecastload>2.5</forecastload><negociate>Yes</negociate><negociateload>7</negociateload><greenenergy>1</greenenergy></usagedata>'
print(xml + '\n')

# test pack
imf = pack(xml)
print(printableByteArray(imf) + '\n')

# test unpack
xml = unpack(imf)
print(xml + '\n')

# test repacking
imf = pack(xml)
print(printableByteArray(imf) + '\n')
'''
