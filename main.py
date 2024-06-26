import cv2
from handTrackingModule import handDetector as htm
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)   # width
cap.set(4, 720)    # height
detector = htm(detectionCon=0.8)  # create an instance of hand detector from htm
colorR = (255, 0, 255)       # color of boxes

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=(w, h)):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # if the index finger is in the rectangle
        if cx - w // 2 < cursor[1] < cx + w // 2 and cy - h // 2 < cursor[2] < cy + h // 2:
            self.posCenter = cursor[1], cursor[2]


rect = DragRect([150, 150])
rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flip horizontally
    detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)  # detect landmarks
    if lmList:
        # hand landmark detected
        l = detector.Distance(img, 8, 12, draw=False)
        if l < 45:
            cursor = lmList[8]
            # call the updates here
            for rect in rectList:
                rect.update(cursor)
            colorR = (255, 255, 0)
        else:
            colorR = (255, 0, 255)

    # Draw transparent
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.001  # transparency level
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)