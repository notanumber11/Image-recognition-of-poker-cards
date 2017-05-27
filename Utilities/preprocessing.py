from __future__ import division
import cv2
import matplotlib.pyplot as plt
import numpy as np


class Preprocessing:

    def __init__(self):
        pass

    @staticmethod
    def preprocessing(img):
        # Change red to black
        imgBlack = img

        imgBlack = Preprocessing.changeRedToBlack(img)

        # Image to gray scale
        gray = cv2.cvtColor(imgBlack, cv2.COLOR_BGR2GRAY)

        grayNoise = gray
        # # Removing noise with median blur
        # grayNoise = cv2.medianBlur(gray, 5)
        # grayNoise = cv2.GaussianBlur(img, (5, 5), 0)

        # Improving contrast with contrast
        # create a CLAHE object (Arguments are optional).
        contrastImg = grayNoise
        # histogram
        # contrastImg = cv2.equalizeHist(grayNoise)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # contrastImg = clahe.apply(grayNoise)

        # Thresholding
        # blur = cv2.GaussianBlur(gray, (1, 1), 1000)
        # ret, threshold = cv2.threshold(contrastImg,140 , 255, cv2.THRESH_BINARY_INV)
        # threshold = cv2.adaptiveThreshold(contrastImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # threshold = cv2.adaptiveThreshold(contrastImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)
        ret2, threshold = cv2.threshold(contrastImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # print ret2
        # if(ret2<80):
            # print ret2
            # cv2.imshow("preprocessing",contrastImg)
            # cv2.imshow("preprocessing2", threshold)
            # cv2.waitKey()
            # ret2 = 160
        # ret, threshold = cv2.threshold(contrastImg,ret2 , 255, cv2.THRESH_BINARY_INV)



        # Contours
        imgContours = np.copy(img)
        _, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # contours = sorted(contours, key=cv2.contourArea)
        # cv2.drawContours(imgContours, contours, -1, (0, 255, 255), 2)


        # Utilities.printImages(listImage = [gray,contrastImg,threshold,imgContours])

        return img, gray, threshold, contours

    @staticmethod
    def preprocessingImageFromROI(roi):
        img = np.copy(roi)
        return Preprocessing.preprocessing(img)



    @staticmethod
    def preprocessingImage(pathImage):
        # Read image from path
        img = cv2.imread(pathImage)

        return Preprocessing.preprocessing(img)

    @staticmethod
    def printImages(listImage):


        for image in listImage:
            cv2.imshow("image",image)
            cv2.waitKey()
        # # Test images
        # cv2.imshow("gray",gray)
        # cv2.waitKey()
        # #
        # cv2.imshow("contrastImage",contrastImg)
        # cv2.waitKey()
        #
        # cv2.imshow("threshold",threshold)
        # cv2.waitKey()
        #
        # cv2.imshow("contours",imgContours)
        # cv2.waitKey()

    @staticmethod
    def changeRedToBlack(img):
        img2 = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_range = np.array([0, 100, 100], dtype=np.uint8)
        upper_range = np.array([10, 255, 255], dtype=np.uint8)
        # Threshold the HSV image to get only red colors
        mask1 = cv2.inRange(hsv, lower_range, upper_range)
        lower_range = np.array([170, 100, 100], dtype=np.uint8)
        upper_range = np.array([190, 255, 255], dtype=np.uint8)
        # Threshold the HSV image to get only red colors
        mask2 = cv2.inRange(hsv, lower_range, upper_range)

        #a =  len(np.extract(mask2, mask2)) + len(np.extract(mask1,mask1))
        a = np.count_nonzero(mask2) +np.count_nonzero(mask1)
        percentage = a / (img2.shape[0] * img2.shape[1])
        # print img2.shape
        # print "La cantidad de rojo es ", a
        # print "El porcentaje de rojo es ", percentage


        img2[mask1 == 255] = [0, 0, 0]
        img2[mask2 == 255] = [0, 0, 0]
        return img2

    @staticmethod
    def deleteContours(contours, height, area):
        deleteList = []
        for i in range(0, (len(contours))):
            x, y, w, h = cv2.boundingRect(contours[i])
            # print h
            if (h < height or h > 2 * height):
                deleteList.append(i)

        contoursFiltered = np.delete(contours, deleteList, axis=0)
        # print 'Lenght ', len(contours)
        return contoursFiltered

    @staticmethod
    def printContours1by1(contours, finalImage):
        print "Drawing contours = ", len(contours)
        for cnt in contours:
            img2 = np.copy(finalImage)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(img2, cnt, -1, (0, 0, 255), 2)
            cv2.imshow("image", img2)
            cv2.waitKey()

    @staticmethod
    def obtainCentroid(cnts):
        centroidList = []
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w / 2
            cy = y + h / 2
            # print cx,cy
            centroidList.append([cx, cy])
        return centroidList

    @staticmethod
    def compareContours(cnt1, cnt2):
        x, y, w, h = cv2.boundingRect(cnt1)
        cx1 = x + w / 2
        cy1 = y + h / 2
        x, y, w, h = cv2.boundingRect(cnt2)
        cx2 = x + w / 2
        cy2 = y + h / 2

        # we are in different columns ( sort top to bottom )
        if (cy1 + h / 2 >= cy2):
            # Sort from left to right
            if (cx1 >= cx2):
                return 1
        return -1
