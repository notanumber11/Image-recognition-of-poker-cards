import cv2

from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector
from Utilities.preprocessing import Preprocessing


class ProcessROICharacter:

    def __init__(self):
        self.knn = knearest('MachineLearning/CharacterTraining/samples.data','MachineLearning/CharacterTraining/responses.data')


    def processROICharacter(self,listSamples):

        finalList = []
        i = 0
        for sample in listSamples:
            i+=1
            img, gray, threshold, contours = Preprocessing.preprocessingImageFromROI(sample.ROI)

            width = sample.w
            height = sample.h

            if(width>height):
                temp = width
                width = height
                height = temp

            listValidContours = []
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                # check if the contour has the right size
                if ( h > height ):
                    listValidContours.append(cnt)

            roiDetector = RoiDetector(heightThreshold=height, areaThreshold=height*1.2*3)
            # roiDetector = RoiDetector(heightThreshold=5, areaThreshold=1)

            listStringResults = self.knn.applyKnearestToImg(threshold,listValidContours,roiDetector)

            lenght = len(listStringResults)

            response = None



            if(lenght>0):
                if(lenght == 1):
                    response = listStringResults[0]
                    if(listStringResults[0])=='0':
                        response = 'Q'
                    if (listStringResults[0]=='1'):
                        response = 'J'
                if(lenght>1):
                    if('1' in listStringResults or '0' in listStringResults):
                        response='10'

            if response is not None:
                sample.Character = response
                sample.stringResult = response + " " + sample.label
                finalList.append(sample)


            # else:
            #     print 'processROICharacter ' + 'responseNone'
            #
            #     print 'Response', response , ' Angle = ' , sample.angle
            #     # if i == 24:
            #     #     print 'meh'
            #     # cv2.imshow("processROICharacter", sample.img)
            #     cv2.imshow("processROICharacter", threshold)
            #
            #     cv2.waitKey()

            # for response in listStringResults:
            #     print response

        return finalList