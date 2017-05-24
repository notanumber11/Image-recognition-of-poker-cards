import cv2
from Utilities import utility as aux


class ObtainROICharacters():

    def __init__(self):
        pass

    def obtainNumberResponse(self,img,listSamples,thresholdSize = 0.2):
        for sample in listSamples:
            angle = sample.angle
            rows, cols,_ = img.shape
            M = cv2.getRotationMatrix2D((sample.cx,sample.cy), -angle, 1)
            dst = cv2.warpAffine(img, M, (cols, rows))


            x, y, w, h = sample.x, sample.y, sample.w, sample.h

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



            # w = int(w)
            # h = int(h*1.5)
            cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.circle(dst, (sample.cx,sample.cy), 5, aux.colour)
            cv2.imshow("rotated",dst)

            # cv2.circle(img, (sample.cx, sample.cy), 5, aux.colour)
            # cv2.imshow("img", img)

            cv2.waitKey()
            cv2.destroyAllWindows()