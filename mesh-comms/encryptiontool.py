import rsatools
import aestools

# A simple class that contains a list of tuples that contain
# a CA's IP and itt's current AES key
# It also does decryption work through both AES and RSA tools.
class SecurityTool:

    def _init_(self):
        self.listOfConsumerAgents = []


    #Decrypts the AES key using the TA's private key.
    #Either replaces an old key, or adds the key to the list.
    def addAesKey(packet):

        key = rsatools.decryptRSA(packet[0])
        #iterate through the current list of CA IP AES key pairs
        #Compares the IPs, if it matches replaces the old pair with the new pair
        for i in listOfConsumerAgents:
            if(packet[1]==listOfConsumerAgents[i][1])
                listOfConsumerAgents[i] = (key, packet[1])
                return

        listOfConsumerAgents.append(key, packet[1])
        return

    #Takes in a tuple with the data and IP of the sender
    def decryptAESData(packet):

        for i in listOfConsumerAgents:
            if(packet[1]==listOfConsumerAgents[i][1])

                #decrypt the packet using AES, passing it the encrypted data and current key
                data = aestools.decryptAES(packet[0], listOfConsumerAgents[0])
                return data
        print("CA failed to provide AES key")
        return
