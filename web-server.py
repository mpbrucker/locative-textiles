#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import cv2 as cv

patch_ips = {44: "192.168.1.111"}
cur_patches = {}
clients = set()

# websocket server content
async def on_connection(websocket, path):
    ip_addr = await websocket.recv()
    if not ip_addr in connected_clients:
        connected_clients.push(ip_addr)

start_server = websockets.serve(hello, "192.168.1.107", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()




aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_7X7_50)
aruco_params = cv.aruco.DetectorParameters_create()

def send_new_patch(patch_id):
    ip_addr = patch_ips[patch_id]
    if not ip_addr in connected_clients:
        throw Exception("Corresponding client not connected")



while True:
    (corners, ids, rejected) = cv.aruco.detectMarkers(frame, aruco_dict,
	parameters=aruco_params)
    if ids is not None and ids.shape[0] > 0:

        ids = ids.flatten()
        for patch_id in ids:
            if cur_patches.get(patch_id, None) is None:



name = input("What's your name? ")

await websocket.send(name)

