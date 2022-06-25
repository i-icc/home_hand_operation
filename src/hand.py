import cv2
import mediapipe as mp

class HandDetector():
    # def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        zList = []
        bbox = ()
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                # cx, cy = int(lm.x * w), int(lm.y * h)
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                xList.append(cx)
                yList.append(cy)
                zList.append(cz)
                # print(id, cx, cy)
                lmList.append([id, cx, cy, cz])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            zmin, zmax = min(zList), max(zList)
            bbox = xmin, ymin, zmin, xmax, ymax, zmax
            if draw:
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[3], bbox[4]), 
                                (0, 255, 0), thickness = 2)

        return lmList, bbox