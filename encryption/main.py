# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import base64
import os

import argparse

# argparse
parser = argparse.ArgumentParser(description='Encrypt a message with a password')
parser.add_argument('password', type=str, help='The password to use for encryption')
args = parser.parse_args()

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_salt(lengt=16):
    salt = os.urandom(16)
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
    token = f.encrypt(message)
    return token

if args.password:
    password = args.password
    salt = generate_salt()
    key = generate_key(salt, password.encode())
    encrypted_message = encrypt(key, b"Hello World")
    print(encrypted_message)
