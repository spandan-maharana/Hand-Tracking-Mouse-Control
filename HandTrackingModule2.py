import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo=0, draw=True):
        xList = []
        yList = []
        self.lmList = []
        bbox = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
            bbox = (min(xList), min(yList), max(xList), max(yList))
        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # For thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # For fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, image, draw=True, r=10, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        if draw:
            cv2.line(image, (x1, y1), (x2, y2), (255, 3, 255), t)
            cv2.circle(image, (x1, y1), r, (255, 3, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), r, (255, 3, 255), cv2.FILLED)
            cv2.circle(image, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, image, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    capture = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, image = capture.read()
        image = detector.findHands(image)
        lmList, bbox = detector.findPosition(image, draw=True)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("Image", image)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
