# import pyAesCrypt
# # encryption/decryption buffer size - 64K
# bufferSize = 64 * 1024
# password = "foopassword"
# # encrypt
# pyAesCrypt.encryptFile("warrior_status.log", "warrior_status.log.aes", password, bufferSize)
# # decrypt
# pyAesCrypt.decryptFile("warrior_status.log.aes", "dataout.txt", password, bufferSize)

import uuid
print(uuid.uuid4().hex.upper())