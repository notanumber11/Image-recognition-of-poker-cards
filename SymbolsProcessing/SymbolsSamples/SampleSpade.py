from __future__ import division
import cv2


class SampleSpade:

    minSpadePerimeter = 0.76
    maxSpadePerimeter = 1

    minSpadeAspectRatio = 0.65
    maxSpadeAspectRatio = 0.89

    minBlack = 0.25
    maxBlack = 0.70
    matchShapeThreshold = 0.15


    def __init__(self,SpadeSample):
        self.SpadeSample = SpadeSample


    def isBlack(self, sample):
        return not (self.isRed(sample))
        if (sample.percentageRed > SampleComparison.minRed and sample.percentageRed < self.maxRed):
            return True
        return False

    def isRed(self,sample):
        if(sample.percentageRed>self.minBlack and sample.percentageRed<self.maxBlack):
            return True
        return False


    def isSpadePerimeter(self, sample):
        if (sample.relationPerimeter > self.minSpadePerimeter and sample.relationPerimeter < self.maxSpadePerimeter):
            return True
        return False

    def isSpadeAspectRatio(self,sample):
        if (sample.aspectRatio > self.minSpadeAspectRatio and sample.aspectRatio < self.maxSpadeAspectRatio):
            return True
        return False

    def isSpadeMatchShape(self,sample):
        ret = cv2.matchShapes(self.SpadeSample.cnt, sample.cnt, 1, 0.0)
        if (ret < self.matchShapeThreshold):
            return  True, ret
        return False, ret

    def isSpade(self,sample):
        matchShape,ret = self.isSpadeMatchShape(sample)
        aspectRatio = self.isSpadeAspectRatio(sample)
        perimeter = self.isSpadePerimeter(sample)
        Black = self.isBlack(sample)
        # self.printSpade(aspectRatio, Black, matchShape, perimeter, sample)
        return matchShape and aspectRatio and perimeter and Black

    def printSpade(self, sample):
        print ""
        print "<--------------------------------------------------------->"
        print " --  Spade   ---"
        print  "Is Black ? ", self.isBlack(sample), sample.percentageBlack
        print " Is  Perimeter? ", self.isSpadePerimeter(sample), sample.relationPerimeter
        print " Is  Aspect Ratio? ", self.isSpadeAspectRatio(sample), sample.aspectRatio
        print " Is  match shape? ", self.isSpadeMatchShape(sample)
        if self.isBlack(sample) and self.isSpadePerimeter(sample) and self.isSpadeAspectRatio(sample) and self.isSpadeMatchShape(sample):
            print "Is Spade !"
        else:
            print "Is not Spade !"
        print ""
        print "<--------------------------------------------------------->"
        print ""