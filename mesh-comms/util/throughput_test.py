# Jason Van Kerkhoven
# 14/02/2018
#
# Flags:    -v OR --verbose    ==> toggles verbose on
#           -p OR --pack       ==> pack XML before sending
#           -t OR --test       ==> set number of TCP transmissions
#           -a OR --address    ==> set destination address

# generic imports
import sys
import time
from .. import tcpcomms as comms

# selective printing
def printv(string):
    if verbose:
        print(string)




###############################################################################

# init parameters
xmlFile = ('<usagedata'>
        '<homeid>15</homeid>'
        '<time>01-01-15 15:00</time>'
        '<currentload>1.608475556</currentload>'
        '<forecastload>2.5</forecastload>'
        '<negociate>Yes</negociate>'
        '<negociateload>7</negociateload>'
        '<greenenergy>1</greenenergy>'
        '</usagedata>')
verbose = False
pack = False
numTests = 100
address = 'dead:beef::1'

# check for flags
flags = sys.argv
while (len(flags) > 0):
    flag = flags.pop(0)
    # verbose flag
    if (flag == '-v' or flag == '--verbose'):
        verbose = True
    # imf/xml flag
    elif (flag == '-p' or flag == '--pack'):
        pack = True
    # change tests num flag
    elif (flag == '-t' or flag == '-tests'):
        tests = int(flags.pop(0))
    # change destination
    elif (flag == 'address' or flag == '--address'):
        address = str(flags.pop(0))

# print starting details
printv('------------------------------------------')
printv('File Type:              ' + ('IMF' if pack else 'XML'))
printv('Destination:            ' + address)
printv('Number of Transfers:    ' + str(numTests))
printv('------------------------------------------')

# run approriate number of tests
avTime = 0
minTime = 0
maxTime = 0
server = comms.Server()
for i in range (0,numTests):
    print('end')
