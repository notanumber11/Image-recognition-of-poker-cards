from __future__ import division
import cv2


class SampleSpades:

    minSpadesPerimeter = 0.76
    maxSpadesPerimeter = 0.95

    minSpadesAspectRatio = 0.65
    maxSpadesAspectRatio = 0.89

    minBlack = 0.25
    maxBlack = 0.70
    matchShapeThreshold = 0.15


    def __init__(self,SpadesSample):
        self.SpadesSample = SpadesSample


    def isBlack(self, sample):
        return not (self.isRed(sample))
        if (sample.percentageRed > SampleComparison.minRed and sample.percentageRed < self.maxRed):
            return True
        return False

    def isRed(self,sample):
        if(sample.percentageRed>self.minBlack and sample.percentageRed<self.maxBlack):
            return True
        return False


    def isSpadesPerimeter(self, sample):
        if (sample.relationPerimeter > self.minSpadesPerimeter and sample.relationPerimeter < self.maxSpadesPerimeter):
            return True
        return False

    def isSpadesAspectRatio(self,sample):
        if (sample.aspectRatio > self.minSpadesAspectRatio and sample.aspectRatio < self.maxSpadesAspectRatio):
            return True
        return False

    def isSpadesMatchShape(self,sample):
        ret = cv2.matchShapes(self.SpadesSample.contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isSpades(self,sample):
        matchShape,ret = self.isSpadesMatchShape(sample)
        aspectRatio = self.isSpadesAspectRatio(sample)
        perimeter = self.isSpadesPerimeter(sample)
        Black = self.isBlack(sample)

        # self.printSpades(aspectRatio, Black, matchShape, perimeter, sample)
        return matchShape and aspectRatio and perimeter and Black

    def printSpades(self, aspectRatio, Red, matchShape, perimeter, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  Spades   ---"
        print  "Is Black ? ", self.isBlack(sample), sample.percentageBlack
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