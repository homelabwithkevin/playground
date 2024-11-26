# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import base64
import os
import argparse
import random
import binascii
import codecs

parser = argparse.ArgumentParser(description='Encrypt a message with a password')
parser.add_argument('option', type=str, help='Encrypt/decrypt')
parser.add_argument('password', type=str, help='The password to use for encryption')
args = parser.parse_args()

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_salt(length=16):
    random = os.urandom(length)
    salt = binascii.hexlify(random).decode()
    print(f'Salt: {salt}')
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
    print(f'Encypted Message: {encrypted_message}')
    return encrypted_message

def decrypt(key, message):
    f = Fernet(key)
    decrypted_message = f.decrypt(message)
    # https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
    codec_message = codecs.escape_decode(decrypted_message, "utf-8")[0].decode("utf-8")
    print(f'\nDecrypted Message: \n{codec_message}')
    return codec_message

if args.option and args.password:
    option = args.option
    password = (args.password).encode()

    if option == 'encrypt':
        salt = generate_salt()
        key = generate_key(salt, password)
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break

        message = '\n'.join(lines)

        encrypt(key, message.encode())

    elif option == 'decrypt':
        salt = input('Paste your salt: \n')
        message = input('Paste your encrypted message: \n')
        key = generate_key(salt, password)
        decrypt(key, message.encode())
    else:
        print(f'Invalid option')

