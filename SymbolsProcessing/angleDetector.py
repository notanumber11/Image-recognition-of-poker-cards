from __future__ import division
import numpy as np
import cv2

from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector
import math as math

from Utilities import utility as aux
from Utilities.createSampleImages import drawAngle
from Utilities.preprocessing import Preprocessing


class AngleDetector:



    def __init__(self):
        self.roiDetector = RoiDetector(heightThreshold=20,areaThreshold=100)
        self.knnHearts = knearest('MachineLearning/AngleTraining/hearts_360.data','MachineLearning/AngleTraining/angles.data')
        self.knnSpades = knearest('MachineLearning/AngleTraining/spades_360.data', 'MachineLearning/AngleTraining/angles.data')
        self.knnClubs = knearest('MachineLearning/AngleTraining/clubs_360.data', 'MachineLearning/AngleTraining/angles.data')


    def obtainAngle(self,img,listSamples):
        listFinalSamples = []
        for sample in listSamples:
            if (sample.label == 'S'):
                self.knnSpades.applyKnearestToSample(self.roiDetector,img, sample)
                listFinalSamples.append(sample)
            if (sample.label == 'D'):
                contours = []
                contours.append(sample.cnt)
                angle = self.obtainAngleDiamond(sample.cnt,img)
                angle = int(angle)
                sample.angle = angle
                # print 'Angle in angle detector ', angle

                # img2 = drawAngle(img,contours)
                # cv2.imshow("angleDetector",img2)
                # cv2.waitKey()
                listFinalSamples.append(sample)
        return listFinalSamples

    # def drawAngle(self,img, contours):
    #     centroidList = Preprocessing.obtainCentroid(contours)
    #     imgClone = np.copy(img)
    #     for i, cnt in enumerate(contours):
    #         # drawLine(imgClone,cnt)
    #         angle = self.obtainAngle(cnt, imgClone)
    #         cv2.putText(imgClone, str(int(angle)), (int(centroidList[i][0]), int(centroidList[i][1])), aux.font, aux.size,
    #                     aux.colour, 2, cv2.LINE_AA)
    #
    #     return imgClone

    def obtainAngleDiamond(self,cnt, imgClone):
        point1, point2, point3, point4 = self.obtainExtremePoints(cnt)

        # cv2.line(imgClone, point1, point2, (0, 255, 0), 2)
        # cv2.line(imgClone, point3, point4, (0, 255, 255), 2)

        angle = self.calculateAngle(point1, point2, point3, point4)
        if angle < 0:
            angle = angle + 180
        return angle

    def obtainExtremePoints(self,cnt):
        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

        x, y, w, h = cv2.boundingRect(cnt)
        cx = int(x + w / 2)
        cy = int(y + h / 2)

        if (self.obtainDistance(leftmost, rightmost) > self.obtainDistance(topmost, bottommost)):
            return leftmost, rightmost, (cx, cy), (cx, topmost[1])

        else:
            return topmost, bottommost, (cx, cy), (cx, topmost[1])

    def obtainDistance(self,point1, point2):
        xa = point1[0]
        ya = point1[1]

        xb = point2[0]
        yb = point2[1]

        distance = math.sqrt((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb))
        return distance

    def calculateAngle(self,point1, point2, point3, point4):
        if (point2[0] - point1[0] == 0):
            m1 = 100000000
        else:
            m1 = (point2[1] - point1[1]) / (point2[0] - point1[0])

        if (point4[0] - point3[0] == 0):
            m2 = 100000000
        else:
            m2 = (point4[1] - point3[1]) / (point4[0] - point3[0])
        angle = math.atan((m2 - m1) / (1 + m1 * m2))
        angle = math.degrees(angle)
        print 'CreateSampleImages angle ', angle
        return angle