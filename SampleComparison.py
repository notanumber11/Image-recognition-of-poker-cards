from __future__ import division

import cv2

from Preprocessing import aux as aux
from Samples.Sample import Sample
from Samples.SampleClub import SampleClub
from Samples.SampleDiamond import SampleDiamond
from Samples.SampleHeart import SampleHeart
from Samples.SampleSpade import SampleSpade


class SampleComparison:

    pathClub = "SampleImages/sample_clubs2.jpg"
    pathDiamond = "SampleImages/sample_diamonds2.jpg"
    pathHeart = "SampleImages/sample_heart2.jpg"
    pathSpades = "SampleImages/sample_spades2.jpg"

    # List of symbols
    symbols = ['spades', 'clubs', 'heart', 'diamond']

    def __init__(self, pathClub = pathClub,pathDiamond = pathDiamond,pathHeart = pathHeart,pathSpades=pathSpades):

        # SampleImages
        self.diamond = Sample(pathDiamond)
        self.clubs = Sample(pathClub)
        self.heart = Sample(pathHeart)
        self.spades = Sample(pathSpades)

        # List of samples
        self.listSamples = [self.spades,self.clubs,self.heart,self.diamond]

        self.sampleHeart = SampleHeart(self.heart)
        self.sampleDiamond = SampleDiamond(self.diamond)
        self.sampleClubs = SampleClub(self.clubs)
        self.sampleSpade = SampleSpade(self.spades)

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


    def isSpade(self, sample):
        isSpade = self.sampleSpade.isSpade(sample)
        if isSpade:
            sample.label = 'S'
        return isSpade

    def isClub(self, sample):
        isClub = self.sampleClubs.isClub(sample)
        if isClub:
            sample.label = 'C'
        return isClub

    def isHeart(self, sample):
        isHearts = self.sampleHeart.isHeart(sample)
        if isHearts:
            sample.label = 'H'
        return isHearts 

    def isDiamond(self,sample):
        isDiamond = self.sampleDiamond.isDiamond(sample)
        if isDiamond:
            sample.label = 'D'
        return isDiamond 