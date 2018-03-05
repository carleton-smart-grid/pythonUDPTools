from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

#This is all a very basic implementation of RSA,
#Further work can be done to make it better
#Namely signing with the private key of the sender to authenticate it.
#Also should add passwords to the key file, but fuck that for now.

#Generate a pair of public and private keys saving them in the appropriate file
def generateRSAKeys ():
    key = RSA.generate(2048)
    f = open('key.bin', 'wb')
    fpub = open('publickey.bin', 'wb')
    fpub.write(key.publickey().exportKey('PEM'))
    f.write(key.exportKey('PEM'))
    f.close()
    fpub.close()
    return

#Encrypt passed dat currently only encrpyting with the public key
#private key is not currently used to authenticate data
def encryptRSA( dat):

    keyString = open('publickey.bin', 'rb').read()
    key = RSA.import_key(keyString)
    cipher = PKCS1_OAEP.new(key)
    encryptedData = cipher.encrypt(dat)
    return encryptedData

#Takes the data encrypted with the public key and decrypts it with the private keys
#Public key authentication is not currently written
def decryptRSA( dat):

    keyString = open('key.bin', 'rb').read()
    key = RSA.importKey(keyString)
    cipher = PKCS1_OAEP.new(key)
    unencryptedData = cipher.decrypt(dat)
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
