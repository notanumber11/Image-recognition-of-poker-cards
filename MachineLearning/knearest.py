import cv2
import numpy as np

from Utilities.preprocessing import Preprocessing
from Utilities import utility as aux



class knearest:

    def __init__(self,pathSamples,pathResponses):
        samples = np.loadtxt(pathSamples,np.float32)
        responses = np.loadtxt(pathResponses,np.float32)
        responses = responses.reshape((responses.size,1))
        self.knn = cv2.ml.KNearest_create()
        self.knn.train(samples,cv2.ml.ROW_SAMPLE,responses)

    def checkResults(self,pathResponses, results):
        # Load corrects results from file
        responses = np.loadtxt(pathResponses, np.float32)
        responses = responses.reshape((1, responses.size))

        # Change format results
        results = np.array(results, np.int32)
        results = results.reshape((1,results.size))

        # Checking if the lenght is the same
        if results.size != responses.size:
            print 'Error en el numero de muestras detectadas'
            return

        diff = np.subtract(responses, results)
        # print responses
        # print results
        print np.sum(diff)

    def applyKnearest(self,roiDetector,imgPath,sizeSample = 100,shapeSample = (10, 10)):

        if (shapeSample[0]*shapeSample[1]!=sizeSample):
            print 'Error with parameters sizeSample and shapeSample'
            return -1
        self.shapeSample = shapeSample
        self.sizeSample = sizeSample

        # preprocessing image
        img, gray, thresh, contours = Preprocessing.preprocessingImage(imgPath)
        # sort contours from upper-left to bottom-right
        contours = sorted(contours, cmp=Preprocessing.compareContours)

        out = np.zeros(img.shape, np.uint8)

        resultsTesting = []

        # Obtaining the rois
        roiList,roiPointList = roiDetector.roiDetection(thresh, contours)

        # Find the right position to apply k-nearest
        for i,roi in enumerate(roiList):

           # Resizing the shape
            roismall = cv2.resize(roi,self.shapeSample)
            roismall = roismall.reshape((1,self.sizeSample))
            roismall = np.float32(roismall)

            # Obtaining positions
            x, y, w, h = roiPointList[i][0], roiPointList[i][1], roiPointList[i][2], roiPointList[i][3]

            # Applying algorithm knearest
            retval, results, neigh_resp, dists = self.knn.findNearest(roismall, k = 1)
            string = str((unichr(results[0][0])))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

            # Save results for testing
            resultsTesting.append(results[0][0])

        # End for loop
        # Save results when they are 100% Ok
        # np.savetxt('TextResults/example_test.txt',resultsTesting)
        # checkResults('TextResults/example_test.txt',resultsTesting)
        print "knearest complete"

        cv2.imshow("thresh",thresh)
        cv2.imshow('out',out)
        cv2.waitKey(0)


    def applyKnearestToSample(self,roiDetector,sample,sizeSample = 100,shapeSample = (10, 10)):

        if (shapeSample[0]*shapeSample[1]!=sizeSample):
            print 'Error with parameters sizeSample and shapeSample'
            return -1
        self.shapeSample = shapeSample
        self.sizeSample = sizeSample


        # Obtaining the rois
        roi = roiDetector.roiDetectionCNT(sample)

        if(roi is not None):

           # Resizing the shape
            roismall = cv2.resize(roi,self.shapeSample)
            roismall = roismall.reshape((1,self.sizeSample))
            roismall = np.float32(roismall)

            # Obtaining positions
            # x, y, w, h = roiPointList[i][0], roiPointList[i][1], roiPointList[i][2], roiPointList[i][3]

            # Applying algorithm knearest
            retval, results, neigh_resp, dists = self.knn.findNearest(roismall, k = 1)
            if dists > 999999:
                print 'Error in knearest character'
                return None
            result = (results[0][0])
            return result
        return None

    def applyKnearestToImg(self,threshold,contours,roiDetector,sizeSample = 100,shapeSample = (10, 10)):
        if (shapeSample[0]*shapeSample[1]!=sizeSample):
            print 'Error with parameters sizeSample and shapeSample'
            return -1
        self.shapeSample = shapeSample
        self.sizeSample = sizeSample

        # Init list of results
        listResults = []

        # Obtaining the rois
        roiList, roiPointList = roiDetector.roiDetection(threshold, contours)

        # Find the right position to apply k-nearest
        for i, roi in enumerate(roiList):
            # Resizing the shape
            roismall = cv2.resize(roi, self.shapeSample)
            roismall = roismall.reshape((1, self.sizeSample))
            roismall = np.float32(roismall)

            # Obtaining positions
            x, y, w, h = roiPointList[i][0], roiPointList[i][1], roiPointList[i][2], roiPointList[i][3]

            # Applying algorithm knearest
            retval, results, neigh_resp, dists = self.knn.findNearest(roismall, k=1)


            string = str((unichr(results[0][0])))

            if dists > 999999:
                print 'Error in knearest character'
                continue
            listResults.append(string)


        return listResults