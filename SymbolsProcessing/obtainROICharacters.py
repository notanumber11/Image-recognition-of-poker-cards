import cv2
from Utilities import utility as aux


class ObtainROICharacters():

    def __init__(self):
        pass

    def getROICharacter(self, img, threshold, listSamples, thresholdSize = 0.3):

        finalList = []

        for sample in listSamples:
            angle =  - sample.angle
            rows, cols,_ = img.shape
            M = cv2.getRotationMatrix2D((sample.cx+sample.offSetX,sample.cy+sample.offSetY), angle, 1)
            dst = cv2.warpAffine(img, M, (cols, rows))

            # cv2.imshow("obtainROICharacters",dst)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

            x, y, w, h = sample.x+sample.offSetX, sample.y+sample.offSetY, sample.w, sample.h

            # If the rectangle has more width than height
            if w > h:
                temp = w
                w = h
                h = temp

            # print x, y, w, h
            offSetY = 1.5 * h
            y = int(y - offSetY)
            h = int(h * 1.2)
            diffY = (int)(thresholdSize * h)
            diffX = (int)(thresholdSize * w)
            h = h + diffY * 2
            w = w + diffX * 2
            y = y - diffY
            x = x - diffX

            roi = dst[y:y+h,x:x+w]


            if y < 0 or x < 0:
                continue

            # print y, y + h, x, x + w
            # cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.circle(dst, (sample.cx,sample.cy), 5, aux.colour)
            # cv2.imshow("obtainROICharacters",roi)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

            sample.ROI = roi
            finalList.append(sample)
        return finalList