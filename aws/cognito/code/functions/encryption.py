# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import base64
import os
import argparse
import random
import binascii
import codecs

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_salt(length=16):
    random = os.urandom(length)
    salt = binascii.hexlify(random).decode()
    return salt

def generate_key(salt, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(key, message):
    f = Fernet(key)
    encrypted_message = f.encrypt(message).decode()
    return encrypted_message

def decrypt(key, message):
    f = Fernet(key)
    decrypted_message = f.decrypt(message)
    # https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
    codec_message = codecs.escape_decode(decrypted_message, "utf-8")[0].decode("utf-8")
    print(f'\nDecrypted Message: \n{codec_message}')
    return codec_message

def save_to_file(file, salt, message):
    with open(file, 'a') as f:
        f.write(f'{salt},{message}\n')

    print(f'Saved to file {file}')
