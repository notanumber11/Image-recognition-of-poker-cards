from __future__ import division
import cv2

import numpy as np
from OCR import OCR
import aux as aux
from Sample import Sample
from SampleComparison import SampleComparison


class SampleCreator:

    thresholdArea = 50
    thresholdSize = 0.1
    font = cv2.FONT_HERSHEY_SIMPLEX
    symbolsColour = (0,255,255)
    idColour = (0,255,0)
    sampleComparison = SampleComparison()

    def __init__(self):
        pass


    def obtainImages(self, imgPath = None, img = None):
        if (img is None):
            img = cv2.imread(imgPath)

        else:
            self.img = img


        # Image preparation
        rows,cols,_ = img.shape
        imgBlack = aux.changeRedToBlack(img)
        contours = aux.obtainContours(imgBlack)

        # Draw all the contours
        # cv2.drawContours(img, contours, -1, (0, 255, 255), 2)
        # cv2.imshow("imgContours",img)
        # cv2.waitKey()

        listImgs = []
        listOffSetX = []
        listOffSetY = []

        for cnt in contours[:-1]:
            if(cv2.contourArea(cnt)>SampleCreator.thresholdArea):
                x,y,w,h = cv2.boundingRect(cnt)

                diffY = (int)(SampleCreator.thresholdSize*h)
                diffX = (int)(SampleCreator.thresholdSize*w)
                h = h + diffY*2
                w = w + diffX*2
                y = y - diffY
                x = x - diffX

                if(x>0 and y>0 and (y+h)<rows and (x+w) < cols):
                    sample = img[y:y + h, x:x + w]
                    listImgs.append(sample)
                    listOffSetX.append(x)
                    listOffSetY.append(y)

        return img,listImgs,listOffSetX,listOffSetY


    def obtainSamples(self, imgPath = None, img = None):
        listSamples = []

        img,listImgs,listOffSetX,listOffSetY  = self.obtainImages(imgPath, img)

        for i, img2 in enumerate(listImgs):
            sample = Sample(img = img2, offSetX=listOffSetX[i], offSetY=listOffSetY[i])
            listSamples.append(sample)

        return img,listSamples,listOffSetX,listOffSetY

    # cv2.drawContours(sample.img, sample.contours, -1, (0, 255, 255), 2)
    # aux.fittingLine2(img,sample.contours[0],listOffSetX[i], listOffSetY[i])
    # aux.fittingMinimumRectangle(img,sample.contours[0],listOffSetX[i], listOffSetY[i])
    def testSamples(self,img,listSamples,listOffSetX,listOffSetY):
        maxAngle = 0
        minAngle = 90
        # Testing time !!!
        for i,sample in enumerate(listSamples):


            flagSpades = self.sampleComparison.isSpade(sample)

            flagClubs = self.sampleComparison.isClub(sample)

            flagHearts = self.sampleComparison.isHeart(sample)

            flagDiamonds = self.sampleComparison.isDiamond(sample)


            list = [flagHearts,flagSpades,flagDiamonds,flagClubs]
            if self.TrueXor(list):
                # cv2.putText(img, sample.label, (listOffSetX[i], listOffSetY[i]), self.font, 0.5, self.symbolsColour, 2,cv2.LINE_AA)
                angle = aux.fittingMinimumRectangle(sample.img, sample.contours[0])
                cv2.putText(img, str(int(angle)), (listOffSetX[i], listOffSetY[i]), self.font, 0.5, self.symbolsColour, 2,cv2.LINE_AA)

            isSymbol = flagClubs or flagDiamonds or flagHearts or flagSpades

            # if isSymbol:
            #     angle = aux.fittingMinimumRectangle(sample.img,sample.contours[0])
            #     if angle < 0:
            #         angle = angle * -1
            #
            #     if angle < minAngle and angle > 25:
            #         minAngle = angle
            #
            #     if angle > maxAngle:
            #         maxAngle = angle
            #
            #     print angle
                # self.showSample(sample)

            #     cv2.drawContours(sample.img, sample.contours, 0, (0, 255, 255), 2)
            #     cv2.imshow("sample", sample.img)
            #     cv2.waitKey()
            #     cv2.destroyAllWindows()

            # if not isSymbol:

                # cv2.rectangle(sample.img, (sample.x, sample.y), (sample.x + sample.w, sample.y + sample.h), (255, 255, 0), 2)
                # cv2.drawContours(a, sample.contours, 0, (0, 255, 255), 2)
                # cv2.imshow("sample", a)
                # cv2.waitKey()
                # cv2.destroyAllWindows()
            #     character = self.detectCharacter(img,sample,listOffSetX[i],listOffSetY[i])

            # if not isSymbol:
            #     ocr = OCR()
            #     character = ocr.detectCharacter(img, sample, listOffSetX[i], listOffSetY[i])
        print minAngle,maxAngle

    def showSamples(self,listSamples):
        for sample in listSamples:
            self.showSample(sample)

    def showSample(self,sample):
        cv2.imshow("sample", sample.img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def TrueXor(self,iterable):
        it = iter(iterable)
        return any(it) and not any(it)