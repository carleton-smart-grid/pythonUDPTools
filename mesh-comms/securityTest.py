import aestools
import rsatools
import encryptiontool

#This script test the functionallity of encryptiontool.py
#It tests the function addAesKey() which takes an encrypted AES key and IP (here just a string),
#it tests the ability to add and over-write keys to the CA list
#It also tests the decryptAESData fucnction, by decrypting a packets data after matching it to
#the appropriate AES key

tool = encryptiontool.SecurityTool()
key1 = aestools.generateKey()
key2 = aestools.generateKey()
key3 = aestools.generateKey()
data = b'hello there   '
packet1 = (rsatools.encryptRSA(key1),'hello')
packet2 = (rsatools.encryptRSA(key2),'heythere')
packet3 = (rsatools.encryptRSA(key3),'hello')
data2 = aestools.encryptAES(data, key3)

tool.addAesKey(packet1)
tool.addAesKey(packet2)
tool.printCAList()
tool.addAesKey(packet3)
tool.printCAList()
data3 = tool.decryptAESData((data2, 'hello'))
print(data3)
