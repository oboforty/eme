import os
import sys
import base64
import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


iv = 'psXbHYqZNSdw1EIO44xz5w=='
iv = base64.b64decode(iv)

password = "!!!RS JELSZO!!!"
payload = "The Alan Parsons Project"
payload += ' ' * (16 - len(payload) % 16)


print('payload:', payload)
m = hashlib.new('md5')
m.update(password.encode('ascii'))
key = m.hexdigest().encode('ascii')

print('key:', key)

backend = default_backend()


cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()


cr = encryptor.update(payload.encode('ascii')) + encryptor.finalize()
gargle = base64.b64encode(cr)

print(gargle)
