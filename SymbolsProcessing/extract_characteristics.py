from __future__ import division
import cv2
from SymbolsProcessing.SymbolsSamples.Sample import Sample


class ExtractCharacteristics:

    def __init__(self):
        pass


    def extractCharacteristics(self, listImgs,listTreshold, listContours, listOffSetX,listOffSetY):
        listSamples = []
        for i, img in enumerate(listImgs):

            sample = Sample(img , listTreshold[i], listContours[i], offSetX=listOffSetX[i], offSetY=listOffSetY[i])
            # cv2.imshow("extract_characteristics",sample.img)
            # cv2.waitKey()
            listSamples.append(sample)

        return listSamples


