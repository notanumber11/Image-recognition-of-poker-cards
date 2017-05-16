from __future__ import division

from SymbolsProcessing.SymbolsSamples.Sample import Sample


class ExtractCharacteristics:

    def __init__(self):
        pass


    def extractCharacteristics(self, listImgs, listContours, listOffSetX,listOffSetY):
        listSamples = []
        for i, img in enumerate(listImgs):
            sample = Sample(img , listContours[i], offSetX=listOffSetX[i], offSetY=listOffSetY[i])
            listSamples.append(sample)

        return listSamples


