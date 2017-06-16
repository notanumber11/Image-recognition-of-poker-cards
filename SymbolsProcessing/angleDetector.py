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
        self.roiDetector = RoiDetector(heightThreshold=10,areaThreshold=50)
        self.knnHearts = knearest('MachineLearning/AngleTraining/hearts_360.data','MachineLearning/AngleTraining/angles.data')
        self.knnSpades = knearest('MachineLearning/AngleTraining/spades_360.data', 'MachineLearning/AngleTraining/angles.data')
        self.knnClubs = knearest('MachineLearning/AngleTraining/clubs_360.data', 'MachineLearning/AngleTraining/angles.data')


    def obtainAngle(self,img,listSamples):
        listFinalSamples = []


        for i,sample in enumerate(listSamples):
            # print 'Iteraccion ', i
            # cv2.imshow("angleDetector", sample.img)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            if (sample.label == 'S'):
                angle = self.knnSpades.applyKnearestToSample(self.roiDetector, sample)
            elif (sample.label == 'C'):
                angle = self.knnClubs.applyKnearestToSample(self.roiDetector, sample)
            elif (sample.label == 'H'):
                angle = self.knnHearts.applyKnearestToSample(self.roiDetector, sample)
            elif (sample.label == 'D'):
                contours = []
                contours.append(sample.cnt)
                angle = self.obtainAngleDiamond(sample.cnt,sample,img)

            if angle is None:
                continue

            angle = int(angle)
            sample.angle = angle
            listFinalSamples.append(sample)

        # for s in listFinalSamples:
            # cv2.rectangle(img, (s.x+s.offSetX, s.y+s.offSetY), (s.x+s.offSetX + s.w, s.y+s.offSetY + s.h), (0, 255, 0), 2)

        return listFinalSamples




    def obtainAngleDiamond(self,cnt,sample,img):
        point1, point2, point3, point4 = self.obtainExtremePoints(cnt)
        # self.drawPoint(img,point1[0]+sample.offSetX,point1[1]+sample.offSetY)
        # self.drawPoint(img,point2[0]+sample.offSetX,point2[1]+sample.offSetY)
        # self.drawPoint(img,point3[0]+sample.offSetX,point3[1]+sample.offSetY)
        # self.drawPoint(img,point4[0]+sample.offSetX,point4[1]+sample.offSetY)
        # self.drawLine(img,point1,point2,sample)
        # self.drawLine(img, point3, point4, sample,aux.colour)


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

        # return leftmost,rightmost,topmost,bottommost

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
        return angle

    def drawPoint(self,img,x,y):
        print x,y
        # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(img,(x,y),3, aux.colour, 5)

    def drawLine(self,img,point1,point2,sample,colour =(0, 255, 0) ):
        x = point1[0] + sample.offSetX
        x1 = point2[0] + sample.offSetX
        y = point1[1] + sample.offSetY
        y1= point2[1] + sample.offSetY
        cv2.line(img, (x,y), (x1,y1),colour , 3)