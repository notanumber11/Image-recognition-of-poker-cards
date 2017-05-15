from __future__ import division
import cv2

class RoiDetector:

    def __init__(self,heightThreshold = 50,areaThreshold = 200):
        self.heightThreshold = heightThreshold
        self.areaThreshold = areaThreshold


    def roiDetection(self,thresh,contours):
        roiList = []
        roiPointsList = []
        for cnt in contours:
            if cv2.contourArea(cnt) > self.areaThreshold:
                [x, y, w, h] = cv2.boundingRect(cnt)
                if h > self.heightThreshold and h < self.heightThreshold * 20:
                    # Utilities image
                    roi = thresh[y:y + h, x:x + w]
                    roiList.append(roi)
                    roiPointsList.append((x,y,w,h))

        return roiList,roiPointsList