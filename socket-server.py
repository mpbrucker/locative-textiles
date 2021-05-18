#!/usr/bin/env python

# WS server example

import asyncio
import websockets


class PatchServer():
    def __init__(self):
        self.clients = {}
        start_server = websockets.serve(self.counter, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def update_patch_pos(self, ip_addr, pos):
        if self.clients.get(ip_addr, None) is not None:
            client = self.clients[ip_addr]
            await asyncio.wait(client.send(pos))
        
    async def register(self, websocket):
        self.clients[websocket.host] = websocket
        print(self.clients)
        print("new client")

    async def unregister(self, websocket):
        self.clients.pop(websocket.host, None)
        print(self.clients)
        print("client removed")

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            # await websocket.send(state_event())
            async for message in websocket:
                print(message)
        finally:
            await self.unregister(websocket)

server = PatchServer()

