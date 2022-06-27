import cv2
import mediapipe as mp
import math
import numpy as np


ANGLES = [(4, 3, 2), (3, 2, 1), (8, 7, 6), (7, 6, 5), (6, 5, 0), (12, 11, 10), (11, 10, 9),
          (10, 9, 0), (16, 15, 14), (15, 14, 13), (14, 13, 0), (20, 19, 18), (19, 18, 17), (18, 17, 16)]


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
                              (0, 255, 0), thickness=2)

        return lmList, bbox

    def find_pose(self, img, handNo=0):
        position_list = dict()
        hand_pose = -1
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                position_list[id] = np.array([lm.x, lm.y, lm.z])

            angles = []
            for angle in ANGLES:
                angles.append(get_angle(
                    position_list[angle[0]], position_list[angle[1]], position_list[angle[2]]))
            print(",".join(list(map(str,angles))))
            
        return hand_pose


def get_angle(point1, point2, point3):
    vec_a = point1 - point2
    vec_c = point3 - point2

    length_vec_a = np.linalg.norm(vec_a)
    length_vec_c = np.linalg.norm(vec_c)
    inner_product = np.inner(vec_a, vec_c)
    cos = inner_product / (length_vec_a * length_vec_c)

    rad = np.arccos(cos)
    degree = np.rad2deg(rad)

    return degree