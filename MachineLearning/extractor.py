from __future__ import division

import sys
import numpy as np
import cv2
from Utilities.preprocessing import Preprocessing


# Keys range accepted from the keyboard
keys = [i for i in range(47, 82)]


class Extractor():

    def __init__(self,sizeSample = 100,shapeSample = (10, 10)):

        self.shapeSample = shapeSample
        self.sizeSample = sizeSample

    def pixelClassifier(self, roiDetector, imgPath, labelPath = None):

        self.roiDetector = roiDetector
        # Init variables
        samples = np.empty((0, self.sizeSample))
        responses = []

        # Check if we are using keyboard or file to label the data
        if(labelPath==None):
            keyboard = True
        else:
            keyboard = False
            responses = np.loadtxt(labelPath, np.float32)
            responses = responses.reshape(responses.size, 1)

        # Utilities image
        im, gray, thresh, contours = Preprocessing.preprocessingImage(imgPath)

        contours = sorted(contours, self.compareContours)


        # Showing thesholding
        # cv2.imshow("sample", thresh)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # Obtaining the rois
        roiList,roiPointList = roiDetector.roiDetection(thresh, contours)

        # Loop rois
        for i,roi in enumerate(roiList):
            roismall = cv2.resize(roi, self.shapeSample)
            roismall = roismall.reshape((1, self.sizeSample))

            # Sampling with keyboard
            if keyboard:
                x,y,w,h = roiPointList[i][0],roiPointList[i][1],roiPointList[i][2],roiPointList[i][3]
                imgCopy = im.copy()
                cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (0, 0, 255), 2)

                key = self.getKey(imgCopy)

                print 'La tecla es ', key
                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    responses.append(key)
                    samples = np.append(samples, roismall, 0)
                else:
                    print 'skipping'
            else:
                sample = roismall.reshape((1, self.sizeSample))
                samples = np.append(samples, sample, 0)

        # Put data in the right format when using keyboard
        if keyboard:
            responses = np.array(responses, np.int32)
            responses = responses.reshape(responses.size, 1)

        # Finish training and saving results
        print "training complete"
        np.savetxt('MachineLearning/TrainingData/samples.data', samples)
        np.savetxt('MachineLearning/TrainingData/responses.data', responses)

    def getKey(self,imgCopy):
        cv2.imshow('imgCopy', imgCopy)
        key = cv2.waitKey(0)
        return key

    def compareContours(self, cnt1, cnt2):
        # print 'La altura es ', self.roiDetector.heightThreshold
        x, y, w, h = cv2.boundingRect(cnt1)
        cx1 = x + w / 2
        cy1 = y + h / 2
        x, y, w, h = cv2.boundingRect(cnt2)
        cx2 = x + w / 2
        cy2 = y + h / 2

        # we are in different columns ( sort top to bottom )
        if (cy1 + self.roiDetector.heightThreshold >= cy2):
            # Sort from left to right
            if (cx1 >= cx2):
                return 1
        return -1