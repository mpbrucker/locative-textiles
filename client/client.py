#!/usr/bin/env python

# Raspi patch client

import asyncio
import websockets
import time
import sys
import serial
from motor import setup_motor, vibrate, set_vibrate
from haversine import haversine


setup_motor()

async def pull_location():
    uri = "ws://192.168.1.107:8765"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                    test = await websocket.recv()
                    if test.startswith("found"):
                        vibrate(50, 0.3)
                        time.sleep(0.3)
                        vibrate(50, 0.3)
                        time.sleep(0.2)
                        
                        split_loc = test.split(" ")
                        loc = " ".join(split_loc[2:4])
                        with open("loc.txt", "w+") as loc_file:
                            loc_file.write(loc)

                    elif test == "moved":
                        vibrate(30, 0.05)
                    elif test == "new patch":
                        vibrate(50, 0.3)
    except: 
        print("connection failed")
        time.sleep(1)

def pull_loc():
    with open("loc.txt", "r") as loc_file:
        line = loc_file.readline().strip().split(" ")
        return (float(line[0]), float(line[1]))

def parse_serial(data):
    data = data.split(",")
    lat_val = data[2]
    lat_dir = data[3]
    lat_dec = int(lat_val[0:2]) + float(lat_val[2:])/60
    if lat_dir != 'N':
        lat_dec *= -1

    lon_val = data[4]
    lon_dir = data[5]
    lon_dec = int(lon_val[0:3]) + float(lon_val[3:])/60
    if lon_dir != 'E':
        lon_dec *= -1
    return (lat_dec, lon_dec)
    
async def detect_location():
    # State variables for keeping track of async vibration changes
    cur_vibrating = False
    last_state_change = time.time()
    cur_period = 1000

    last_pulled = time.time()
    cur_loc = pull_loc()
    cur_dist = 1000
    ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=None,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,rtscts=False,xonxoff=False,dsrdtr=False) 
    print("starting serial")
    while True:

        # regularly refresh the location stored the file
        if time.time() - last_pulled > 60:
            cur_loc = pull_loc()
            last_pulled = time.time()

        # parse the serial data from GPS
        try: 
            data=ser.readline().strip().decode("utf-8") 
            if data.startswith("$GNGGA"):
                loc = parse_serial(data)
                cur_dist = haversine(loc, cur_loc)
                cur_period = 1+(cur_dist*5)
                # If we're in range, start vibrating
        except:
            print("data read failed")
        
        if cur_dist < 0.7:
            time_elapsed = time.time() - last_state_change
            if not cur_vibrating:
                if time_elapsed > cur_period:
                    set_vibrate(50)
                    last_state_change = time.time()
                    cur_vibrating = True
                    print("on")
            elif time_elapsed > 0.3:
                set_vibrate(0)
                last_state_change = time.time()
                cur_vibrating = False
                print("off")
            # print(cur_period)
            # print(cur_vibrating)
            # print(time_elapsed)

            # vibrate(50, 0.3)
            # time.sleep(0.3)
            # vibrate(0, 0.3)
            # time.sleep(1+(cur_dist*5))

        # print(cur_dist)


async def main_loop():
    # await pull_location()
    await detect_location()


asyncio.get_event_loop().run_until_complete(main_loop())
