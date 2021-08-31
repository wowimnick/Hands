import cv2
import time
import os
import numpy as np
import module as m

# Initialization
w, h = 1280, 720

vid = cv2.VideoCapture(0)
vid.set(3, w)
vid.set(4, h)

detect = m.searchHands()
tips = [4, 8, 12, 16, 20]
check = [2, 6, 10, 14, 18]

while True:
    result, frame = vid.read()
    detect.findHands(frame)
    lmList = detect.pos(frame, draw=False)

    if len(lmList) != 0:
        fingers = []
        if lmList[tips[0]][0] < lmList[check[0]][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        for finger in range(1, 5):

            if lmList[tips[finger]][1] > lmList[check[finger]][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        cv2.putText(frame, str(fingers.count(1)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255),
                    3)
    cv2.imshow("Img", frame)
    cv2.waitKey(1)
