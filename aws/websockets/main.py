#!/usr/bin/env python

import os
import asyncio

from websockets.sync.client import connect
from dotenv import load_dotenv

load_dotenv()

ws_server = os.getenv('WS_SERVER')

from websockets.asyncio.client import connect

async def hello():
    async with connect(ws_server) as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print(f">>> {name}")
        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":

    asyncio.run(hello())
