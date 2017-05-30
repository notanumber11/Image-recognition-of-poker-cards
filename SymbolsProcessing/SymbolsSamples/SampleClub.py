from __future__ import division
import cv2


class SampleClub:

    minClubPerimeter = 0.80
    maxClubPerimeter = 1.4

    minClubAspectRatio = 0.85
    maxClubAspectRatio = 1.05

    minBlack = 0.25
    maxBlack = 0.70
    matchShapeThreshold = 0.15


    def __init__(self,clubsSample):
        self.clubsSample = clubsSample


    def isBlack(self, sample):
        return not (self.isRed(sample))
        if (sample.percentageRed > SampleComparison.minRed and sample.percentageRed < self.maxRed):
            return True
        return False

    def isRed(self,sample):
        if(sample.percentageRed>self.minBlack and sample.percentageRed<self.maxBlack):
            return True
        return False


    def isClubPerimeter(self, sample):
        if (sample.relationPerimeter > self.minClubPerimeter and sample.relationPerimeter < self.maxClubPerimeter):
            return True
        return False

    def isClubAspectRatio(self,sample):
        if (sample.aspectRatio > self.minClubAspectRatio and sample.aspectRatio < self.maxClubAspectRatio):
            return True
        return False

    def isClubMatchShape(self,sample):
        ret = cv2.matchShapes(self.clubsSample.cnt, sample.cnt, 1, 0.0)
        self.matchShape = ret
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isClub(self,sample):
        matchShape,ret = self.isClubMatchShape(sample)
        aspectRatio = self.isClubAspectRatio(sample)
        perimeter = self.isClubPerimeter(sample)
        Black = self.isBlack(sample)

        # self.printClub(aspectRatio, Black, matchShape, perimeter, sample)
        return matchShape and aspectRatio and perimeter and Black

    def printClub(self, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  CLUBS   ---"
        print  "Is Black ? ", self.isBlack(sample), sample.percentageBlack
        print " Is  Perimeter? ", self.isClubPerimeter(sample), sample.relationPerimeter
        print " Is  Aspect Ratio? ", self.isClubAspectRatio(sample), sample.aspectRatio
        print " Is  match shape? ", self.isClubMatchShape(sample)
        matchShape,_ = self.isClubMatchShape(sample)
        if matchShape and self.isClubAspectRatio(sample) and self.isClubPerimeter(sample) and self.isBlack(sample):
            print "Is Club !"
        else:
            print "Is not Club !"
        print ""
        print "<--------------------------------------------------------->"
        print ""