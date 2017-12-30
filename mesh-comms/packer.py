##############################################################################
#
# Class:             packer.py
# Author:            Jason Van Kerkhoven
# Date of Update:    28/12/2017
# Version:           0.1.0
#
# Purpose:           TODO
#
# Arguments:         N/A
#
# Flags:             N/A
#
##############################################################################



#import external libraries
import xml.etree.ElementTree as et
import struct


# convert float to 4B bytearray (LSB at 0)
def floatToByteArr(num):
    return bytearray(struct.pack('f', num))

# convert int to bitstring
def intToBits(num, minLength):
    bits = '{0:b}'.format(num)
    while (len(bits) < minLength):
        bits = '0' + bits
    return bits


# pack data from XML
# RETURNS a bytearray in IMF
def pack(xmlContents):
    # init xml root element and inf returnable
    root = et.fromstring(xmlContents)
    inf = bytearray()

    # parse homeid, default 0
    homeid = root.find('./homeid')
    if (homeid != None):
        homeid = int(homeid.text) if homeid.text != None else 0
        if (homeid > 255 or homeid < 0):
            homeid = 0
    else:
        homeid = 0
    # add homid to inf
    inf.extend((homeid,))

    # parse time, default 0
    time = root.find('./time')
    if (time != None):
        timeRaw = time
        time = (time.text) if time.text != None else 0
    else:
        time = 0;
    # add time to inf TODO actually convert to UNIX stamp
    inf.extend((0xde,0xad,0xbe,0xef))

    # parse current load, default 0
    currentload = root.find('./currentload')
    if (currentload != None):
        currentload = float(currentload.text) if currentload.text != None else 0.0
    else:
        currentload = 0.0
    # add currentload
    inf.extend(floatToByteArr(currentload))

    # parse forecast load, default 0
    forecastload = root.find('./forecastload')
    if (forecastload != None):
        forecastload = float(forecastload.text) if forecastload.text != None else 0.0
    else:
        forecastload = 0.0
    # add forecastload
    inf.extend(floatToByteArr(forecastload))

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
    inf.extend((int('0b'+byte, 2),))


    # return
    return inf



# unpack data into XML
# RETURNS a XML-esque UTF-8 character string
def unpack(packetContents):
    printv('general kenobi')


# tests
##########################################################################
print('starting...')

# test pack
inf = pack('<usagedata><homeid>15</homeid><time>01-01-15 15:00</time><currentload>1.608475556</currentload><forecastload>2.5</forecastload><negociate>Yes</negociate><negociateload>7</negociateload><greenenergy>1</greenenergy></usagedata>')
print([ "0x%02x" % b for b in inf ])

# test unpack
