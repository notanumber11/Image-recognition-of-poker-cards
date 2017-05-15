from __future__ import division

from SymbolsProcessing.SymbolsSamples.Sample import Sample


class ExtractCharacteristics:

    def __init__(self):
        pass


    def extractCharacteristics(self, listImgs, listOffSetX,listOffSetY):
        listSamples = []
        for i, img2 in enumerate(listImgs):
            sample = Sample(img = img2, offSetX=listOffSetX[i], offSetY=listOffSetY[i])
            listSamples.append(sample)

        return listSamples


