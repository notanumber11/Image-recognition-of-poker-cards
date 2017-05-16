from __future__ import division
import cv2



class SampleDiamond:

    minDiamondRelationArea = 0.38
    maxDiamondRelationArea = 0.57
    minRed = 0.25
    maxRed = 0.7
    matchShapeThreshold = 0.15

    def __init__(self,diamondSample):
        self.diamondSample = diamondSample


    def isRed(self,sample):
        if(sample.percentageRed>self.minRed and sample.percentageRed<self.maxRed):
            return True
        return False

    def isDiamondRelationArea(self, sample):
        if (sample.relationArea > self.minDiamondRelationArea and sample.relationArea < self.maxDiamondRelationArea):
            return True
        return False



    def isDiamondsMatchShape(self,sample):
        ret = cv2.matchShapes(self.diamondSample.cnt, sample.cnt, 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isDiamond(self, sample):
        matchShape, ret = self.isDiamondsMatchShape(sample)
        red = self.isRed(sample)
        relationArea = self.isDiamondRelationArea(sample)

        # self.printDiamond(matchShape, red, relationArea, sample)

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