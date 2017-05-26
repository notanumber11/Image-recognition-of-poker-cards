import cv2

from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector
from Utilities.preprocessing import Preprocessing


class ProcessROICharacter:

    def __init__(self):
        # self.knn = knearest('MachineLearning/CharacterTraining/samples.data','MachineLearning/CharacterTraining/responses.data')
        self.knn = knearest('MachineLearning/TrainingData/samples.data','MachineLearning/TrainingData/responses.data')


    def processROICharacter(self,listSamples):

        finalList = []
        i = 0
        for sample in listSamples:



            i+=1
            img, gray, threshold, contours = Preprocessing.preprocessingImageFromROI(sample.ROI)

            # cv2.drawContours(img, contours, -1, (0, 255, 255), 2)
            # cv2.imshow("processROICharacter", img)
            # cv2.waitKey()

            width = sample.w
            height = sample.h

            if(width>height):
                temp = width
                width = height
                height = temp

            listValidContours = []
            # for cnt in contours:
            #     x,y,w,h = cv2.boundingRect(cnt)
            #     # check if the contour has the right size
            #     if ( h > height ):
            #         listValidContours.append(cnt)
            listValidContours = contours


            roiDetector = RoiDetector(heightThreshold=height, areaThreshold=0)
            # roiDetector = RoiDetector(heightThreshold=5, areaThreshold=1)


            listStringResults = self.knn.applyKnearestToImg(threshold,listValidContours,roiDetector)

            lenght = len(listStringResults)

            response = None



            if(lenght>0):
                if(lenght == 1):
                    response = listStringResults[0]
                    # if (listStringResults[0]=='1'):
                    #     response = 'J'
                if(lenght>1):
                    if('1' in listStringResults and '0' in listStringResults):
                        response='10'
                    else:
                        response = listStringResults[0]
                        if(listStringResults[0]=='1'):
                            i = 0
                            while(listStringResults[i]=='1' and i < lenght):
                                i +=1
                                response = listStringResults[i]
                if(response=='1'):
                    response = None
                # if(response == '0'):
                #     response = 'Q'

                # print '----------------------'
                # for string in listStringResults:
                #     print string


                # if response == 'J':
                #     cv2.imshow("processROICharacter", threshold)
                #     cv2.waitKey()

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




            # for response in listStringResults:
            #     print response

        return finalList