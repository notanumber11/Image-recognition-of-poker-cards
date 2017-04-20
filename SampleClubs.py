from __future__ import division
import cv2


class SampleClubs:

    minClubsAspectRatio = 0.85
    maxClubsAspectRatio = 1.05

    minClubsPerimeter = 0.85
    maxClubsPerimeter = 1.4

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


    def isClubsPerimeter(self, sample):
        if (sample.relationPerimeter > self.minClubsPerimeter and sample.relationPerimeter < self.maxClubsPerimeter):
            return True
        return False

    def isClubsAspectRatio(self,sample):
        if (sample.aspectRatio > self.minClubsAspectRatio and sample.aspectRatio < self.maxClubsAspectRatio):
            return True
        return False

    def isClubsMatchShape(self,sample):
        ret = cv2.matchShapes(self.clubsSample.contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

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