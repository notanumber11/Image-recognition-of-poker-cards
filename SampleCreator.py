from __future__ import division
import cv2
import aux as aux
from Sample import Sample
from SampleComparison import SampleComparison


class SampleCreator:

    thresholdArea = 80
    thresholdSize = 0.1


    sampleComparison = SampleComparison()

    def __init__(self):
        pass


    def obtainImages(self, imgPath = None, img = None):
        if (img == None):
            img = cv2.imread(imgPath)

        else:
            self.img = img

        rows,cols,_ = img.shape
        imgBlack = aux.changeRedToBlack(img)
        contours = aux.obtainContours(imgBlack)

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

        for sample in listImgs:
            sampleBlack = aux.changeRedToBlack(sample)
            contoursSample = aux.obtainContours(sampleBlack)
            # cv2.drawContours(sample, contoursSample, 0, (0, 255, 255), 2)



        return listImgs,listOffSetX,listOffSetY


    def obtainSamples(self,imgPath = None, img = None):
        listSamples = []
        image = cv2.imread(imgPath)




        listImgs,listOffSetX,listOffSetY  = self.obtainImages(imgPath,img)
        for i,img in enumerate(listImgs):
            sample = Sample(img = img,offSetX=listOffSetX[i],offSetY=listOffSetY[i])
            cv2.drawContours(sample.img, sample.contours, 0, (0, 255, 255), 2)
            cv2.imshow("sample",sample.img)

            # Testing time !!!



            flag = self.sampleComparison.isSpades(sample)

            if ( flag == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, "Spades", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)


            flag = self.sampleComparison.isClubs(sample)

            if ( flag == True):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, "Clubs", (listOffSetX[i], listOffSetY[i]), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)
            # if ( flag == False):
            #     cv2.waitKey()

            listSamples.append(sample)


        cv2.imshow("sample", image)
        cv2.waitKey()
        return listSamples
