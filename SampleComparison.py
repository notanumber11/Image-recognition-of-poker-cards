from __future__ import division
import cv2
import aux as aux
from Sample import Sample


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
        cv2.imshow("img",img2)
        cv2.waitKey()

    minBlack = 0.25
    maxBlack = 0.70


    def isBlack(self,sample):
        return not(self.isRed(sample))
        if(sample.percentageRed>SampleComparison.minRed and sample.percentageRed<self.maxRed):
            return True
        return False
    
    



    minClubsPerimeter = 0.85
    maxClubsPerimeter = 1.4
    
    minSpadesPerimeter = 0.76
    maxSpadesPerimeter = 0.95
    

    def isClubsPerimeter(self, sample):
        if(sample.relationPerimeter>self.minClubsPerimeter and sample.relationPerimeter<self.maxClubsPerimeter):
            return True
        return False
    
    
    def isSpadesPerimeter(self, sample):
        if(sample.relationPerimeter>self.minSpadesPerimeter and sample.relationPerimeter<self.maxSpadesPerimeter):
            return True
        return False

    minClubsAspectRatio = 0.85
    maxClubsAspectRatio = 1.05

    minSpadesAspectRatio = 0.65
    maxSpadesAspectRatio = 0.89
    
    def isClubsAspectRatio(self,sample):
        if (sample.aspectRatio > self.minClubsAspectRatio and sample.aspectRatio < self.maxClubsAspectRatio):
            return True
        return False

    def isSpadesAspectRatio(self, sample):
        if (sample.aspectRatio > self.minSpadesAspectRatio and sample.aspectRatio < self.maxSpadesAspectRatio):
            return True
        return False

    matchShapeThreshold = 0.15

    def isSpadesMatchShape(self,sample):
        ret = cv2.matchShapes(self.listSamples[0].contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret


    def isClubsMatchShape(self,sample):
        ret = cv2.matchShapes(self.listSamples[1].contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret



    
    
    def isDiamondsMatchShape(self,sample):
        ret = cv2.matchShapes(self.listSamples[3].contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isSpades(self,sample):
        matchShape,ret = self.isSpadesMatchShape(sample)
        aspectRatio = self.isSpadesAspectRatio(sample)
        perimeter = self.isSpadesPerimeter(sample)
        Black = self.isBlack(sample)
        self.printSpades(aspectRatio, Black, matchShape, perimeter, sample)
        return matchShape and aspectRatio and perimeter and Black
    
    
    def printSpades(self, aspectRatio, Red, matchShape, perimeter, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  Spades   ---"
        print  "Is Red ? ", self.isBlack(sample), sample.percentageBlack
        print " Is  Perimeter? ", self.isSpadesPerimeter(sample), sample.relationPerimeter
        print " Is  Aspect Ratio? ", self.isSpadesAspectRatio(sample), sample.aspectRatio
        print " Is  match shape? ", self.isSpadesMatchShape(sample)
        if matchShape and aspectRatio and perimeter and Red:
            print "Is Spades !"
        else:
            print "Is not Spades !"
        print ""
        print "<--------------------------------------------------------->"
        print ""
    
    
    def isClubs(self,sample):
        matchShape,ret = self.isClubsMatchShape(sample)
        aspectRatio = self.isClubsAspectRatio(sample)
        perimeter = self.isClubsPerimeter(sample)
        Black = self.isBlack(sample)

        # self.printClubs(aspectRatio, Black, matchShape, perimeter, sample)
        return matchShape and aspectRatio and perimeter and Black

    def printClubs(self, aspectRatio, Red, matchShape, perimeter, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  CLUBS   ---"
        print  "Is Black ? ", self.isBlack(sample), sample.percentageBlack
        print " Is  Perimeter? ", self.isClubsPerimeter(sample), sample.relationPerimeter
        print " Is  Aspect Ratio? ", self.isClubsAspectRatio(sample), sample.aspectRatio
        print " Is  match shape? ", self.isClubsMatchShape(sample)
        if matchShape and aspectRatio and perimeter and Red:
            print "Is Clubs !"
        else:
            print "Is not Clubs !"
        print ""
        print "<--------------------------------------------------------->"
        print ""

    def isDiamondRelationArea(self, sample):
        if (sample.relationArea > self.minDiamondRelationArea and sample.relationArea < self.maxDiamondRelationArea):
            return True
        return False
    
    minDiamondRelationArea = 0.38
    maxDiamondRelationArea = 0.57

    
    def isDiamond(self,sample):
        matchShape,ret = self.isDiamondsMatchShape(sample)
        red = self.isRed(sample)
        relationArea = self.isDiamondRelationArea(sample)

        #self.printDiamond(matchShape, red, relationArea, sample)
        
        return matchShape and relationArea and red

    def printDiamond(self, matchShape, red, relationArea, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  Diamonds   ---"
        print  "Is red ? ", self.isRed(sample), sample.percentageRed
        print " Is  RelationArea? ", self.isDiamondRelationArea(sample), sample.relationArea
        print " Is  match shape? ", self.isDiamondsMatchShape(sample)
        if matchShape and relationArea and red:
            print "Is Diamonds !"
        else:
            print "Is not Diamonds !"
        print ""
        print "<--------------------------------------------------------->"
        print ""





    # Heart zone

    minHeartRelationArea = 0.57
    maxHeartRelationArea = 0.7

    minRed = 0.25
    maxRed = 0.7

    def isHeart(self,sample):
        matchShape,ret = self.isHeartsMatchShape(sample)
        red = self.isRed(sample)
        relationArea = self.isHeartRelationArea(sample)
        # self.printHeart(matchShape, red, relationArea, sample)
        return matchShape and relationArea and red

    def printHeart(self, matchShape, red, relationArea, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  Hearts   ---"
        print  "Is red ? ", self.isRed(sample), sample.percentageRed
        print " Is  RelationArea? ", self.isHeartRelationArea(sample), sample.relationArea
        print " Is  match shape? ", self.isHeartsMatchShape(sample)
        if matchShape and relationArea and red:
            print "Is Hearts !"
        else:
            print "Is not Hearts !"
        print ""
        print "<--------------------------------------------------------->"
        print ""

    def isHeartsMatchShape(self,sample):
        ret = cv2.matchShapes(self.listSamples[2].contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isHeartRelationArea(self, sample):
        if (sample.relationArea > self.minHeartRelationArea and sample.relationArea < self.maxHeartRelationArea):
            return True
        return False

    def isRed(self,sample):
        if(sample.percentageRed>SampleComparison.minRed and sample.percentageRed<self.maxRed):
            return True
        return False