from __future__ import division

import cv2


class GenerateCandidates:
    def __init__(self):
        pass

    def generateCandidates(self, img,threshold, contours, thresholdArea=50, thresholdSize=0.1):
        contours = sorted(contours, key=cv2.contourArea)
        self.thresholdArea = thresholdArea
        self.thresholdSize = thresholdSize
        rows, cols, _ = img.shape
        listROIs = []
        listOffSetX = []
        listOffSetY = []
        listContours = []
        listThreshold = []

        for cnt in contours[:-1]:
            if (cv2.contourArea(cnt) > self.thresholdArea):
                x, y, w, h = cv2.boundingRect(cnt)

                diffY = (int)(self.thresholdSize * h)
                diffX = (int)(self.thresholdSize * w)
                h = h + diffY * 2
                w = w + diffX * 2
                y = y - diffY
                x = x - diffX

                if (x > 0 and y > 0 and (y + h) < rows and (x + w) < cols):
                    sample = img[y:y + h, x:x + w]
                    thresh = threshold[y:y + h, x:x + w]
                    listROIs.append(sample)
                    listOffSetX.append(x)
                    listOffSetY.append(y)
                    listContours.append(cnt)
                    listThreshold.append(thresh)

        return img, listROIs,listThreshold, listContours, listOffSetX, listOffSetY
