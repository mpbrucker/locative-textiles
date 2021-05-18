#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import cv2 as cv
start_server = websockets.serve(hello, "192.168.1.107", 8765)

patch_ips = {44: "192.168.1.111"}
connected_clients = 

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_7X7_50)
aruco_params = cv.aruco.DetectorParameters_create()


while True:
    (corners, ids, rejected) = cv.aruco.detectMarkers(frame, aruco_dict,
	parameters=aruco_params)
    if ids is not None and ids.shape[0] > 0:

        ids = ids.flatten()


name = input("What's your name? ")

await websocket.send(name)

