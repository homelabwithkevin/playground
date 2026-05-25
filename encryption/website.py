import os
import binascii

from fastapi import FastAPI, Query

app = FastAPI()

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
