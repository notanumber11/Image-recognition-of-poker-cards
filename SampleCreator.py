from __future__ import division
import cv2

import numpy as np

import aux as aux
from Sample import Sample
from SampleComparison import SampleComparison


class SampleCreator:

    thresholdArea = 50
    thresholdSize = 0.1
    font = cv2.FONT_HERSHEY_SIMPLEX
    symbolsColour = (0,255,255)
    idColour = (255,255,0)
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

            flagSpades = self.sampleComparison.isSpade(sample)

            flagClubs = self.sampleComparison.isClub(sample)

            flagHearts = self.sampleComparison.isHeart(sample)

            flagDiamonds = self.sampleComparison.isDiamond(sample)




            list = [flagHearts,flagSpades,flagDiamonds,flagClubs]
            if self.TrueXor(list):
                cv2.putText(img, sample.label, (listOffSetX[i], listOffSetY[i]), self.font, 0.5, self.symbolsColour, 2,cv2.LINE_AA)
                # aux.fittingLine2(img,sample.contours[0],listOffSetX[i], listOffSetY[i])
                # aux.fittingMinimumRectangle(img,sample.contours[0],listOffSetX[i], listOffSetY[i])

            isSymbol = flagClubs or flagDiamonds or flagHearts or flagSpades

            if not isSymbol:

                vis = np.concatenate((sample.img,sample.img), axis=1)
                vis = np.concatenate((vis,vis), axis=1)
                vis = np.concatenate((vis, vis), axis=1)
                character = self.detectCharacter(vis)

                if character is not None:
                    cv2.putText(img, character, (listOffSetX[i], listOffSetY[i]), self.font, 0.5, self.idColour, 2,cv2.LINE_AA)


        # print 'Ejecutando test '
        # cv2.imshow("sample", img)
        # cv2.waitKey()


    def showSamples(self,listSamples):
        for sample in listSamples:
            cv2.imshow("sample", sample.img)
            cv2.waitKey()
            cv2.destroyAllWindows()


    def detectCharacter(self,img):
        from PIL import Image
        from pytesseract import image_to_string

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)




        pil_im = Image.fromarray(cv2_im)



        # print image_to_string(Image.open('test.png'))
        result = []
        result = image_to_string(pil_im, lang='eng')
        

        if len (result) > 0 and ((ord(result[0])>47 and ord(result[0])< 58) or (ord(result[0])>64 and ord(result[0])< 91)):
            # print 'Detectado ' + result

            return result[0]
        return None

    def TrueXor(self,iterable):
        it = iter(iterable)
        return any(it) and not any(it)