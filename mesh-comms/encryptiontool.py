import rsatools
import aestools


# A simple class that contains a list of tuples that contain
# a CA's IP and itt's current AES key
# It also does decryption work through both AES and RSA tools.
class SecurityTool(object):
    def __init__(self):
        self.listOfConsumerAgents = []


    #Decrypts the AES key using the TA's private key.
    #Either replaces an old key, or adds the key to the list.
    def addAesKey(self, packet):

        key = rsatools.decryptRSA(packet[0])
        #iterate through the current list of CA IP AES key pairs
        #Compares the IPs, if it matches replaces the old pair with the new pair
        for i in range (0, len(self.listOfConsumerAgents)):
            if(packet[1]==self.listOfConsumerAgents[i][1]):
                self.listOfConsumerAgents[i] = (key, packet[1])
                return

        self.listOfConsumerAgents.append((key, packet[1]))
        return

    #Takes in a tuple with the data and IP of the sender
    def decryptAESData(self, packet):

        for i in range(0, len(self.listOfConsumerAgents)):

            if(packet[1]==self.listOfConsumerAgents[i][1]):
                #decrypt the packet using AES, passing it the encrypted data and current key
                data = aestools.decryptAES(packet[0], self.listOfConsumerAgents[i][0])
                return data
        print("CA failed to provide AES key")
        return

    def printCAList(self):
        print (self.listOfConsumerAgents)
