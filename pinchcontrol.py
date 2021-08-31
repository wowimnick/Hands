import cv2
import time
import numpy as np
import module as m
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialization
w, h = 1280, 720

vid = cv2.VideoCapture(0)
vid.set(3, w)
vid.set(4, h)

detect = m.searchHands()
audiodevice = AudioUtilities.GetSpeakers()
interface = audiodevice.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange = volume.GetVolumeRange()
minVol = volrange[0]
maxVol = volrange[1]

while True:
    result, frame = vid.read()
    frame = detect.findHands(frame)
    lmList = detect.pos(frame, draw=False)
    if len(lmList) != 0:
        # Position of thumb and index finger tips
        x1, y1 = lmList[8][0], lmList[8][1]
        x2, y2 = lmList[4][0], lmList[4][1]
        # Find middle point of the line
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1) # Calculate the length of the line
        vol = np.interp(length, [50, 300], [minVol, maxVol]) # Interpolation

        cv2.line(frame, (x1, y1), (x2, y2), (255, 100, 255), 3) # Line drawn between thumb and index finger tips
        cv2.putText(frame, str(length), (cx, cy+50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255),
                    2) # Volume count above middle circle


        if length < 50:
            cv2.circle(frame, (cx, cy), 15, (0, 0, 255), cv2.FILLED) # Circle turning red, indicating mute/low volume
        else:
            cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
            volume.SetMasterVolumeLevel(vol, None)
            print(int(length), vol)

    cv2.imshow("Img", frame)
    cv2.waitKey(1)
