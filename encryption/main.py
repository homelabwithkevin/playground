# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import base64
import os
import argparse
import random
import binascii

parser = argparse.ArgumentParser(description='Encrypt a message with a password')
parser.add_argument('option', type=str, help='Encrypt/decrypt')
parser.add_argument('password', type=str, help='The password to use for encryption')
args = parser.parse_args()

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b'temporary'

def generate_salt(length=16):
    random = os.urandom(length)
    salt = binascii.hexlify(random)
    print(f'Salt: {salt}')
    return salt

def generate_key(salt, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(key, message):
    f = Fernet(key)
    encrypted_message = f.encrypt(message)
    print(f'Encypted Message: {encrypted_message}')
    return encrypted_message

def decrypt(key, message):
    f = Fernet(key)
    decrypted_message = f.decrypt(message)
    print(f'Decrypted Message: {decrypted_message}')
    return decrypted_message

if args.option and args.password:
    option = args.option
    password = (args.password).encode()

    if option == 'encrypt':
        # salt = generate_salt()
        key = generate_key(salt, password)
        message = input('Enter the message to encrypt: ')
        encrypt(key, message.encode())

    elif option == 'decrypt':
        # salt = b'2a56e4c43535a3e7a3ac9692e5094aad'
        key = generate_key(salt, password)
        message = b'gAAAAABnRSawMpsKjV4aclf_NSsX37bx42-AhuZkfwImOdpxsF_T0Jkw1vJ2K3B4cJA42zO4Yyy15Zu8PXw7_OZSPhebl1yHU3itJTjViXPZMTVUO9oTv0w='
        decrypt(key, message)
    else:
        print(f'Invalid option')

