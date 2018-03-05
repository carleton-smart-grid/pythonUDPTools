from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

#Intra mesh format is currently 14 bytes long, may change.
DATA_LENGTH = 14
#AES key is 16 bytes for a 128 bit key.
KEY_LENGTH = 16

#returns the new 16 byte key, useful to have to key itself to send to CAs
def generateKey():
    key = get_random_bytes(KEY_LENGTH)
    return key

#Returns the AES cipher object
#def generateAESCipher(key):
#    cipher = AES.new(key, AES.MODE_ECB)
#    return cipher

#Encypts data with the AES key,
#Pads the data to the nearest 16 byte multiple.
#Currently, data is fixed at 14 bytes in the IMF
def encryptAES( data, key):

    cipher = AES.new(key, AES.MODE_ECB)
    data = data + b'00'
    encryptedData = cipher.encrypt(data)
    return encryptedData

#decrypts using the AES key, removing padding before returning
def decryptAES( data, key):

    cipher = AES.new(key, AES.MODE_ECB)
    decryptedData = cipher.decrypt(data)
    unpaddedData = decryptedData[:DATA_LENGTH]
    return unpaddedData

def testAES():
    key = generateKey()
    dataA = b'fourteen bytes'
    cipher = generateCipher(key)
    dataB = encryptAES(dataA, cipher)
    print(dataB)
    dataC = decryptAES(dataB, cipher)
    print(dataC)

#Additional little code samples for varible packet size, given an ability to end with two null bytes.
##Zero pad blocks to make it encryptable
#for x in range(0, (blockSize - packetLength)):
#    text = text + b'0'
#
##Strip padding from end of data
#for y in range(len(data) - 1, 0, -1):
#    if data[y] != '0':
#        break
#unpaddedData = data[:y+1]
