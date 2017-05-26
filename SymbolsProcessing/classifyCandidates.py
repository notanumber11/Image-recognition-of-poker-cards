from __future__ import division
import cv2

from SymbolsProcessing.SymbolsSamples.Sample import Sample
from SymbolsProcessing.SymbolsSamples.SampleClub import SampleClub
from SymbolsProcessing.SymbolsSamples.SampleDiamond import SampleDiamond
from SymbolsProcessing.SymbolsSamples.SampleHeart import SampleHeart
from SymbolsProcessing.SymbolsSamples.SampleSpade import SampleSpade
from Utilities.preprocessing import Preprocessing


class ClasifyCandidates:
    thresholdArea = 50
    thresholdSize = 0.1
    font = cv2.FONT_HERSHEY_SIMPLEX
    symbolsColour = (0, 255, 255)
    idColour = (0, 255, 0)


    pathClub = "SampleImages/sample_clubs2.jpg"
    pathDiamond = "SampleImages/sample_diamonds2.jpg"
    pathHeart = "SampleImages/sample_hearts2.jpg"
    pathSpades = "SampleImages/sample_spades2.jpg"

    # List of symbols
    symbols = ['spades', 'clubs', 'heart', 'diamond']

    def __init__(self, pathClub = pathClub,pathDiamond = pathDiamond,pathHeart = pathHeart,pathSpades=pathSpades):

        # SampleImages
        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathDiamond)
        self.diamond = Sample(img,threshold,contours[0])
        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathClub)
        self.clubs = Sample(img,threshold,contours[0])
        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathHeart)
        self.heart = Sample(img,threshold,contours[0])
        img, gray, threshold, contours = Preprocessing.preprocessingImage(pathSpades)
        self.spades = Sample(img,threshold,contours[0])

        # List of samples
        self.listSamples = [self.spades,self.clubs,self.heart,self.diamond]

        self.sampleHeart = SampleHeart(self.heart)
        self.sampleDiamond = SampleDiamond(self.diamond)
        self.sampleClubs = SampleClub(self.clubs)
        self.sampleSpade = SampleSpade(self.spades)


    def clasifyCandidates(self, img, listSamples):

        listFinal = []
        for i, sample in enumerate(listSamples):

            flagSpades = self.isSpade(sample)

            flagClubs = self.isClub(sample)

            flagHearts = self.isHeart(sample)

            flagDiamonds = self.isDiamond(sample)

            list = [flagHearts, flagSpades, flagDiamonds, flagClubs]
            if self.TrueXor(list):
                # cv2.putText(img, sample.label, (sample.offSetX, sample.offSetY), self.font, 0.5, self.symbolsColour, 2, cv2.LINE_AA)
                listFinal.append(sample)
            isSymbol = flagClubs or flagDiamonds or flagHearts or flagSpades

            # if not isSymbol:
            #     cv2.imshow("classifyCandidates.py",sample.img)
            #     self.sampleSpade.printSpade(sample)
            #     cv2.waitKey()
            sample.stringResult = sample.label
        return listFinal

    def showSamples(self, listSamples):
        for sample in listSamples:
            self.showSample(sample)

    def showSample(self, sample):
        cv2.imshow("sample", sample.img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def TrueXor(self, iterable):
        it = iter(iterable)
        return any(it) and not any(it)

    def printInfo(self):
        for i in range(len(self.listSamples)):
            print "------------> ", self.symbols[i]
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

    def isDiamond(self, sample):
        isDiamond = self.sampleDiamond.isDiamond(sample)
        if isDiamond:
            sample.label = 'D'
        return isDiamond