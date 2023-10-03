import cv2
from CustomModules.HandTrackModule import HandDetector
import math
import numpy as np
from screen_brightness_control import set_brightness

minBrt = 0
maxBrt = 100
brt = 0
brtBar = 400

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.7)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        # print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)


        length = math.hypot(x2-x1,y2-y1)
        print(length)

        brt = np.interp(length, [50,250],[minBrt,maxBrt])
        brtBar = np.interp(length, [50, 250], [400, 150])

        set_brightness(brt)

        if length<50:
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50,int(brtBar)), (85,400), (0,255,0),cv2.FILLED)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    cv2.imshow("Image",img)
    cv2.waitKey(1)