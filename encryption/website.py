import os
import binascii
import base64
from pydantic import BaseModel
from fastapi import FastAPI, Query, Form
from fastapi.responses import HTMLResponse

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

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Encryption Tool</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/htmx.org@2.0.4"></script>
    </head>
    <body class="bg-gray-100 py-12">
        <div class="max-w-6xl mx-auto px-4">
            <h1 class="text-4xl font-bold text-center mb-12 text-gray-800">Encryption Tool</h1>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Encrypt Panel -->
                <div class="bg-white rounded-lg shadow-md p-8">
                    <h2 class="text-2xl font-bold mb-6 text-gray-700">Encrypt</h2>
                    <form hx-post="/encrypt/form" hx-target="#encrypt-result" hx-swap="innerHTML" class="space-y-4">
                        <div>
                            <label for="encrypt-password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                            <input type="password" id="encrypt-password" name="password" required class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label for="encrypt-message" class="block text-sm font-medium text-gray-700 mb-2">Message</label>
                            <textarea id="encrypt-message" name="message" required rows="6" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition">Encrypt</button>
                    </form>
                    <div id="encrypt-result" class="mt-6"></div>
                </div>

                <!-- Decrypt Panel -->
                <div class="bg-white rounded-lg shadow-md p-8">
                    <h2 class="text-2xl font-bold mb-6 text-gray-700">Decrypt</h2>
                    <form hx-post="/decrypt/form" hx-target="#decrypt-result" hx-swap="innerHTML" class="space-y-4">
                        <div>
                            <label for="decrypt-password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                            <input type="password" id="decrypt-password" name="password" required class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label for="decrypt-salt" class="block text-sm font-medium text-gray-700 mb-2">Salt</label>
                            <input type="text" id="decrypt-salt" name="salt" required class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label for="decrypt-message" class="block text-sm font-medium text-gray-700 mb-2">Encrypted Message</label>
                            <textarea id="decrypt-message" name="encrypted_message" required rows="6" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-md transition">Decrypt</button>
                    </form>
                    <div id="decrypt-result" class="mt-6"></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

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

@app.post("/encrypt/form", response_class=HTMLResponse)
def encrypt_form(password: str = Form(...), message: str = Form(...)):
    try:
        salt = generate_salt()
        key = generate_key(salt, password)
        encrypted_message = encrypt(key, message)
        return f"""
        <div class="bg-green-50 border border-green-200 rounded-md p-4">
            <h3 class="font-bold text-green-800 mb-3">Encryption Successful</h3>
            <div class="space-y-2 text-sm">
                <div>
                    <label class="font-semibold text-gray-700">Salt:</label>
                    <div class="bg-white p-2 rounded border border-gray-300 break-all">{salt}</div>
                </div>
                <div>
                    <label class="font-semibold text-gray-700">Encrypted Message:</label>
                    <div class="bg-white p-2 rounded border border-gray-300 break-all">{encrypted_message}</div>
                </div>
            </div>
        </div>
        """
    except Exception as e:
        return f"""
        <div class="bg-red-50 border border-red-200 rounded-md p-4">
            <h3 class="font-bold text-red-800">Error</h3>
            <p class="text-red-700 text-sm">{str(e)}</p>
        </div>
        """

@app.post("/decrypt/form", response_class=HTMLResponse)
def decrypt_form(password: str = Form(...), salt: str = Form(...), encrypted_message: str = Form(...)):
    try:
        key = generate_key(salt, password)
        decrypted_message = decrypt(key, encrypted_message)
        return f"""
        <div class="bg-green-50 border border-green-200 rounded-md p-4">
            <h3 class="font-bold text-green-800 mb-3">Decryption Successful</h3>
            <div class="space-y-2 text-sm">
                <div>
                    <label class="font-semibold text-gray-700">Decrypted Message:</label>
                    <div class="bg-white p-2 rounded border border-gray-300 whitespace-pre-wrap">{decrypted_message}</div>
                </div>
            </div>
        </div>
        """
    except Exception as e:
        return f"""
        <div class="bg-red-50 border border-red-200 rounded-md p-4">
            <h3 class="font-bold text-red-800">Error</h3>
            <p class="text-red-700 text-sm">{str(e)}</p>
        </div>
        """
