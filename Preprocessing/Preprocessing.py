from __future__ import division
import cv2
import matplotlib.pyplot as plt
import numpy as np

import aux as aux

class Preprocessing:

    def __init__(self):
        pass

    def preprocessingImage(self,pathImage):
        # Read image from path
        img = cv2.imread(pathImage)

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

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrastImg = clahe.apply(grayNoise)


        # Thresholding
        ret, threshold = cv2.threshold(contrastImg,180 , 255, cv2.THRESH_BINARY)
        # threshold = cv2.adaptiveThreshold(contrastImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # threshold = cv2.adaptiveThreshold(contrastImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)
        ret2, threshold = cv2.threshold(contrastImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # print ret2


        # Contours
        imgContours = np.copy(img)
        _, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 255), 2)


        Preprocessing.printImages(listImage = [gray,contrastImg,threshold,imgContours])

    @staticmethod
    def printImages(listImage):

        # titles = ['gray', 'contrast',
        #           'threshold', 'contours']
        # images = [img1, img2, img3, img4]
        # for i in xrange(4):
        #     plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        #     plt.title(titles[i])
        #     plt.xticks([]), plt.yticks([])
        # plt.show()


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