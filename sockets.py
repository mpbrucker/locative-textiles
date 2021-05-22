#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from patch import capture

class PatchServer():
    def __init__(self):
        self.clients = {}
        self.start_server = websockets.serve(self.counter, "192.168.1.107", 8765)
        print('testing')
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()

    async def update_patch_pos(self, ip_addr, pos):
        if self.clients.get(ip_addr, None) is not None:
            client = self.clients[ip_addr]
            await asyncio.wait(client.send(pos))

    async def send_client_message(self, ip_addr, msg):
        if self.clients.get(ip_addr, None) is not None:
            client = self.clients[ip_addr]
            await asyncio.wait([client.send(msg)])
        
    async def register(self, websocket):
        self.clients[websocket.remote_address[0]] = websocket
        print(self.clients)
        print("new client")

    async def unregister(self, websocket):
        self.clients.pop(websocket.host, None)
        print(self.clients)
        print("client removed")

    async def counter(self, websocket, path):
        print('test3')
        await self.register(websocket)
        # register(websocket) sends user_event() to websocket
        await capture(self.send_client_message)

if __name__ == '__main__':
    server = PatchServer()
