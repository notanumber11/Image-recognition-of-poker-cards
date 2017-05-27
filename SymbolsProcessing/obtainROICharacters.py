import cv2
from Utilities import utility as aux
from copy import deepcopy

class ObtainROICharacters():

    def __init__(self):
        pass

    def getROICharacter(self, img, threshold, listSamples, thresholdSize = 0.2):

        finalList = []

        diamondList = []

        for sample in listSamples:
            if sample.label == 'D':
                sampleCopy = deepcopy(sample)
                sampleCopy.angle = sampleCopy.angle + 180
                diamondList.append(sampleCopy)

        listSamples.extend(diamondList)


        for sample in listSamples:
            angle =  - sample.angle
            rows, cols,_ = img.shape
            M = cv2.getRotationMatrix2D((sample.cx+sample.offSetX,sample.cy+sample.offSetY), angle, 1)
            dst = cv2.warpAffine(img, M, (cols, rows))
            dstThreshold = cv2.warpAffine(threshold, M, (cols, rows))


            x, y, w, h = sample.x+sample.offSetX, sample.y+sample.offSetY, sample.w, sample.h

            # If the rectangle has more width than height
            if w > h:
                temp = w
                w = h
                h = temp

            # print x, y, w, h
            offSetY = 1.6 * h
            y = int(y - offSetY)
            h = int(h * 1.2)
            diffY = (int)(thresholdSize * h)
            diffX = (int)(thresholdSize * w)
            h = h + diffY * 2
            w = w + diffX * 2
            y = y - diffY
            x = x - diffX

            roi = dst[y:y+h,x:x+w]
            roiThreshold = dstThreshold[y:y+h,x:x+w]

            # cv2.imshow("obtainROICharacters1",roi)
            # cv2.imshow("obtainROICharacters",roiThreshold)
            # cv2.waitKey()
            # cv2.destroyAllWindows()


            if y < 0 or x < 0:
                continue


            sample.ROI = roi
            finalList.append(sample)
        return finalList