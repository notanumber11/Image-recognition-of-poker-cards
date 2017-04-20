from __future__ import division
import cv2
import aux as aux
from Sample import Sample
from SampleClubs import SampleClubs
from SampleDiamond import SampleDiamond
from SampleHeart import SampleHeart
from SampleSpades import SampleSpades


class SampleComparison:

    pathClub = "Samples/sample_clubs2.jpg"
    pathDiamond = "Samples/sample_diamonds2.jpg"
    pathHeart = "Samples/sample_heart2.jpg"
    pathSpades = "Samples/sample_spades2.jpg"

    # List of symbols
    symbols = ['spades', 'clubs', 'heart', 'diamond']

    def __init__(self, pathClub = pathClub,pathDiamond = pathDiamond,pathHeart = pathHeart,pathSpades=pathSpades):

        # Path
        self.pathClub = pathClub
        self.pathDiamond = pathDiamond
        self.pathHeart = pathHeart
        self.pathSpades = pathSpades

        # Samples
        self.diamond = Sample(pathDiamond)
        self.clubs = Sample(pathClub)
        self.heart = Sample(pathHeart)
        self.spades = Sample(pathSpades)

        # List of samples
        self.listSamples = [self.spades,self.clubs,self.heart,self.diamond]

        self.sampleHeart = SampleHeart(self.heart)
        self.sampleDiamond = SampleDiamond(self.diamond)
        self.sampleClubs = SampleClubs(self.clubs)
        self.sampleSpades = SampleSpades(self.spades)

        # self.printInfo()

    def printInfo(self):
        for i in range(len(self.listSamples)):
            print "------------> ",SampleComparison.symbols[i]
            print 'Red = ', self.listSamples[i].percentageRed, 'Red = ', self.listSamples[i].percentageRed
            # print "Area symbol = ", self.listSamples[i].contourArea
            # print "Area rectangle ", self.listSamples[i].rectangleArea
            print "Relation area ", self.listSamples[i].relationArea
            
            # print "perimeter symbol = ", self.listSamples[i].contourPerimeter
            # print "perimeter rectangle ", self.listSamples[i].rectanglePerimeter
            print "Relation perimeter ", self.listSamples[i].relationPerimeter

            print "Aspect Ratio = ", self.listSamples[i].aspectRatio

    def compareMatchShape(self, imgPath):
        font = cv2.FONT_HERSHEY_SIMPLEX


        image = Sample(imgPath)
        img2 = image.img.copy()
        # cv2.drawContours(img2, image.contours, -1, (255, 0, 0), 1)
        # print len(image.contours)
        # Loop all the contours
        for i in range(len(image.contours)):
            if(cv2.contourArea(image.contours[i])<50):
                continue
            matchShapeThreshold = 0.13
            choice = -1
            for j in range(len(self.listSamples)):
                ret = cv2.matchShapes(self.listSamples[j].contours[0], image.contours[i], 1, 0.0)
                #print SampleComparison.symbols[j] , ret
                if(ret < matchShapeThreshold):
                    matchShapeThreshold = ret
                    choice = j;
                    # cv2.imshow("img",image.img)
                    # cv2.waitKey()
            if(choice != -1):
                # Drawing the answer
                cx, cy = aux.extractSingleCentroid(image.contours[i])
                cv2.putText(img2, self.symbols[choice], (cx, cy), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)

                #print "Resultado --> ", SampleComparison.symbols[choice]

        # cv2.drawContours(img2, self.listSamples[choice].contours, 0, (0, 255, 255), 2)
        # cv2.drawContours(img2, image.contours, i, (0, 255, 255), 2)
        # cv2.imshow("img",img2)
        # cv2.waitKey()

    def isSpades(self, sample):
        return self.sampleSpades.isSpades(sample)

    def isClubs(self, sample):
        return self.sampleClubs.isClubs(sample)

    def isHeart(self, sample):
        return self.sampleHeart.isHeart(sample)

    def isDiamond(self,sample):
        return self.sampleDiamond.isDiamond(sample)