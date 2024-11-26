# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import numpy as np
import HandTrackingModule2 as htm
import time
import autopy

wCam = 640  # Width of Camera screen
hCam = 480  # Height of Camera screen
frameR = 200  # frame reduction
smoothening = 4  # Smoothening the values
pTime = 0
plocX, plocY = 0, 0  # previous location of x and y
clocX, clocY = 0, 0  # current location of x and y
capture = cv2.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr,hScr)

while True:
    # 1. Find the hand landmarks
    success, image = capture.read()
    image = detector.findHands(image)
    lmList, bbox = detector.findPosition(image, draw=True)

    # 2. Get the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(image, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 2, 255), 2)
        # 4. Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert the coordinates
            x3 = np.interp(x1, (frameR, wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR),(0,hScr))
            # 6. Smoothen values
            clocX = plocX+(x3-plocX)/smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(image, (x1, y1), 13, (255, 2, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8. Both index and middle fingers are up: Clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, image, lineInfo = detector.findDistance(8, 12, image)
            # 10. Click mouse if distance is short
            if length<40:
                cv2.circle(image, (lineInfo[4], lineInfo[5]), 13, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display
    cv2.imshow("Image", image)
    cv2.waitKey(1)
