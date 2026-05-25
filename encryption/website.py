import os
import binascii
import base64
from pydantic import BaseModel
from fastapi import FastAPI, Query

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = FastAPI()

class EncryptRequest(BaseModel):
    password: str
    message: str

class DecryptRequest(BaseModel):
    password: str
    salt: str
    encrypted_message: str

def generate_salt(length: int = 16) -> str:
    random = os.urandom(length)
    salt = binascii.hexlify(random).decode()
    return salt

def generate_key(salt: str, password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt(key: bytes, message: str) -> str:
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode()).decode()
    return encrypted_message

def decrypt(key: bytes, message: str) -> str:
    f = Fernet(key)
    decrypted_message = f.decrypt(message.encode()).decode()
    return decrypted_message

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/salt")
def get_salt(length: int = Query(16)):
    salt = binascii.hexlify(os.urandom(length)).decode('utf-8')
    return {"salt": salt}

@app.post("/encrypt")
def encrypt_message(request: EncryptRequest):
    salt = generate_salt()
    key = generate_key(salt, request.password)
    encrypted_message = encrypt(key, request.message)
    return {"salt": salt, "encrypted_message": encrypted_message}

@app.post("/decrypt")
def decrypt_message(request: DecryptRequest):
    key = generate_key(request.salt, request.password)
    decrypted_message = decrypt(key, request.encrypted_message)
    return {"decrypted_message": decrypted_message}
