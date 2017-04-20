from __future__ import division
import cv2
import aux as aux
from Sample import Sample
from SampleComparison import SampleComparison


class SampleCreator:

    thresholdArea = 50
    thresholdSize = 0.1


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


    def testSamples(self,img,listSamples,listOffSetX,listOffSetY):

        # Testing time !!!
        for i,sample in enumerate(listSamples):
            # cv2.drawContours(sample.img, sample.contours, -1, (0, 255, 255), 2)
            # cv2.imshow("test", sample.img)
            # cv2.waitKey()

            flagSpades = self.sampleComparison.isSpades(sample)
            if (flagSpades == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "Spades", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)

            flagClubs = self.sampleComparison.isClubs(sample)
            if (flagClubs == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "Clubs", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)


            flagHearts = self.sampleComparison.isHeart(sample)
            if (flagHearts == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "Hearts", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)

            flagDiamonds = self.sampleComparison.isDiamond(sample)
            if (flagDiamonds == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "Diamonds", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)

            # if ( flagSpades == False):
            #     cv2.imshow("sample", sample.img)
            #     cv2.waitKey()

            # if (flagClubs or flagDiamonds or flagHearts or flagSpades):
            #     cv2.imshow("sample", sample.img)
            #     cv2.waitKey()

        # print 'Ejecutando test '
        # cv2.imshow("sample", img)
        # cv2.waitKey()


    def showSamples(self,listSamples):
        for sample in listSamples:
            cv2.imshow("sample", sample.img)
            cv2.waitKey()
            cv2.destroyAllWindows()