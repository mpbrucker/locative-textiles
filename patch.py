#!/usr/bin/env python

# WS server example

import numpy as np
import cv2 as cv
import asyncio
import time

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Match the ARuco tag ID to the corresponding client IP address
patch_ips = {44: "192.168.1.111"}


aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_7X7_50)
aruco_params = cv.aruco.DetectorParameters_create()
proj_corners = np.zeros((4,2))
MAP_CORNER_LIST = [[0,0],[1280,0],[1280,720],[0, 720]]

# The boundary latitude/longitude corresponding to the map area
X_COORD = (123.456, 456.567)
Y_COORD = (123.456, 456.789)

# Updates the corner entries in the list of points for the homography matrix
def get_patch_corners(corners, ids):
    patches = {}
    for (corner, id) in zip(corners, ids):
        corners_list = corner.reshape((4,2))

        # We have two sets of AR tags, one for the projector alignment and one for the actual piece
        if id < 15:
            proj_corners[id-11] = corners_list[id-11]
        if id > 40:
            patches[id] = corners_list
    return patches


# Processes a webcam frame and, if a patch is found, calls the corresponding server callback
async def capture(callback):
    is_found = False
    frames_out = 0
    cur_patches = {}

    while True:
        ret, frame = cap.read()
        (corners, ids, rejected) = cv.aruco.detectMarkers(frame, aruco_dict,
        parameters=aruco_params)

        # Divide the list of AR tags into calibration and patch tags
        if ids is not None and ids.shape[0] > 0:
            ids = ids.flatten()
            patch_corners = get_patch_corners(corners, ids)

        # Perspective transform to the corners of the map AR tags
        if np.count_nonzero(proj_corners) == 8:
            pts_dst = np.array(MAP_CORNER_LIST)
            h_proj, status = cv.findHomography(proj_corners, pts_dst)
            frame_proj = cv.warpPerspective(frame, h_proj, (1280, 720)) # img size is based on 4 px per stitch

            # Iterate through each patch tag and find its location on the map
            for patch_id in patch_corners.keys():
                corners_list = patch_corners[patch_id]

                top_left = corners_list[0]
                bottom_right = corners_list[2]
                center = (top_left+bottom_right)/2

                cv.circle(frame_proj, (int(center[0]), int(center[1])), 5, (255, 0, 0), 2)

                # remap the x/y frame coordinates to the physical map coordinates
                new_center_x = np.interp(center[0], (0, 1280), X_COORD)
                new_center_y = np.interp(center[1], (0, 720), Y_COORD)
                print("{} {}".format(new_center_x, new_center_y))
                print(cur_patches)
                # Based on current state of patch, send callback message(s)
                if cur_patches.get(patch_id, None) is None:
                    await callback(patch_ips[patch_id], "new patch")
                    cur_patches[patch_id] = {"frames_stopped": 1, "center": center}
                else:
                    cur_center = cur_patches[patch_id]["center"]
                    diff = np.linalg.norm(cur_center-center)
                    if diff > 1:
                        cur_patches[patch_id]["frames_stopped"] = 1
                        await callback(patch_ips[patch_id], "moved")
                        time.sleep(0.05)
                    else:
                        cur_patches[patch_id]["frames_stopped"] += 1
                        # If the patch has remained in the same place for long enough, we can send a message the location is locked in
                        if cur_patches[patch_id]["frames_stopped"] > 60 and not is_found:
                            is_found = True
                            await callback(patch_ips[patch_id], "found at {} {}".format(new_center_x, new_center_y))

                    cur_patches[patch_id]["center"] = center
            frame = frame_proj
        else:
            frames_out += 1
            if frames_out > 30:
                cur_patches = {}


        cv.imshow("Detected Circle", frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()



