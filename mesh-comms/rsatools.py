from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

#This is all a very basic implementation of RSA,
#Further work can be done to make it better
#Namely signing with the private key of the sender to authenticate it.
#Also currently using absolute paths to what is effectively a random directory.

#Test paths
#KEY_PATH = 'key.bin'
#PUBLIC_KEY_PATH = 'publickey.bin'
#PI directory paths
KEY_PATH = '/home/pi/SmartGrid/key.bin'
PUBLIC_KEY_PATH = '/home/pi/SmartGrid/publickey.bin'

#Generate a pair of public and private keys saving them in the appropriate file
def generateRSAKeys ():
    key = RSA.generate(2048)
    f = open(KEY_PATH, 'wb')
    fpub = open(PUBLIC_KEY_PATH, 'wb')
    fpub.write(key.publickey().exportKey('PEM'))
    f.write(key.exportKey('PEM'))
    f.close()
    fpub.close()
    return

#Encrypt passed dat currently only encrpyting with the public key
#private key is not currently used to authenticate data
def encryptRSA( dat):

    keyString = open(PUBLIC_KEY_PATH, 'rb').read()
    key = RSA.importKey(keyString)
    cipher = PKCS1_OAEP.new(key)
    encryptedData = cipher.encrypt(dat)
    return encryptedData

#Takes the data encrypted with the public key and decrypts it with the private keys
#Public key authentication is not currently written
def decryptRSA( dat):

    keyString = open(KEY_PATH, 'rb').read()
    key = RSA.importKey(keyString)
    cipher = PKCS1_OAEP.new(key)
    unencryptedData = cipher.decrypt(bytes(dat))
    return unencryptedData

#must have already generated keys to use the test.
def simpleTestRSA():
    data = b'1234567890123456'
    encryptedData = encryptRSA(data)
    print( len(encryptedData))
    decryptedData = decryptRSA(encryptedData)
    if(data == decryptedData):
        print ('It works')
    else:
        print ('We are doomed')
