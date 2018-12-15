import os
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


chunksize=1024*1024

fn_orig = 't.zip'
fn_targ = 't.lef'
fn_back = 't2.zip'

password = '!!!RS_JELSZO!!!'



backend = default_backend()
# convert pw to 16, 24 or 32 bytes & IV to 16 bytes, pad the rest

# todo: itt: kidolgoz jobban, automatikus scaling?
"""
PW key    IV size
48 32     16
40 32     8+pad
24 22+pad 2+pad
16 14+pad 2+pad
10 8+pad  2+pad
"""
# if len(password) > 48:   s1 = 32; s2 = 16
# elif len(password) > 40: s1 = 32; s2 = 8
# elif len(password) > 32: s1 = 30; s2 = 8
# elif len(password) > 24: s1 = 14; s2 = 8
# elif len(password) > 16: s1 = 14; s2 = 2
# elif len(password) > 10: s1 = 14; s2 = 2

# todo: itt: ez csak 11 meretu jelszora muxik, scale up!
s1,s2 = password[:8], password[8:]
key = (b'%' * (16-len(s1))) + s1.encode('utf-8')
iv = s2.encode('utf-8') + (b'0' * (16-len(s2)))
#iv = b'1234567812345678'
#key = os.urandom(32)
#iv = os.urandom(16)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()




# ---------------------------------------------------
# ENCRYPT:
with open(fn_orig, 'rb') as infile:
    with open(fn_targ, 'wb') as outfile:

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += ' ' * (16 - len(chunk) % 16)

            outfile.write(encryptor.update(chunk))
        outfile.write(encryptor.finalize())
# ---------------------------------------------------
# DECRYPT
# todo: this is kinda doomed to fail, store orig_size in DB!
origsize = os.path.getsize(fn_targ)

with open(fn_targ, 'rb') as infile:
    with open(fn_back, 'wb') as outfile:

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            outfile.write(decryptor.update(chunk))

        outfile.write(decryptor.finalize())
        outfile.truncate(origsize)
# ---------------------------------------------------
