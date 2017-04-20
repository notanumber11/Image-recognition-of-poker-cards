from __future__ import division
import cv2



class SampleHeart:

    minHeartRelationArea = 0.57
    maxHeartRelationArea = 0.7
    minRed = 0.25
    maxRed = 0.7
    matchShapeThreshold = 0.15

    def __init__(self,heartSample):
        self.heartSample = heartSample


    def isHeart(self,sample):
        matchShape,ret = self.isHeartsMatchShape(sample)
        red = self.isRed(sample)
        relationArea = self.isHeartRelationArea(sample)
        # self.printHeart(matchShape, red, relationArea, sample)
        return matchShape and relationArea and red

    def isRed(self,sample):
        if(sample.percentageRed>SampleHeart.minRed and sample.percentageRed<self.maxRed):
            return True
        return False

    def isHeartsMatchShape(self,sample):
        ret = cv2.matchShapes(self.heartSample.contours[0], sample.contours[0], 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isHeartRelationArea(self, sample):
        if (sample.relationArea > self.minHeartRelationArea and sample.relationArea < self.maxHeartRelationArea):
            return True
        return False

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