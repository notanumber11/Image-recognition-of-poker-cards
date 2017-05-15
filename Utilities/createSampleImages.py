from __future__ import division
import cv2
import numpy as np

# Properties
from Utilities.Preprocessing import Preprocessing
import math as math

samplesPerLine = 30
numberOfSamples = 360
gradeStep = 360 / numberOfSamples

# Thresholds
heightThreshold = 80
areaThreshold = 150

# Drawing variables
font = cv2.FONT_HERSHEY_SIMPLEX
colour = (0, 255, 255)
fontSize = 0.8

# Method to create samples with different angles
def createSamples(imgpath,imgOut):
    if (numberOfSamples % samplesPerLine):
        print 'Error: samples per line and number of samples should be multiple'
        return

    if (360 % gradeStep):
        print 'Error: 360 and number of samples should be multiple'
        return

    print 'Number of samples ', numberOfSamples
    print 'Grade step ', gradeStep


    img,gray,threshold,contours = Preprocessing.preprocessingImage(imgpath)

    rowsGlobal, colsGlobal, _ = img.shape

    visHorizontalImage = img
    visHorizontalThreshold = threshold
    firstTime = True

    for i in range(1, numberOfSamples + 1):
        M = cv2.getRotationMatrix2D((colsGlobal / 2, rowsGlobal / 2), i * gradeStep, 1)
        dst = cv2.warpAffine(img, M, (colsGlobal, rowsGlobal))
        dstThreshold = cv2.warpAffine(threshold, M, (colsGlobal, rowsGlobal))

        # Change line
        if (i % (samplesPerLine) == 0):
            if (firstTime):
                finalImage = visHorizontalImage
                finalThreshold = visHorizontalThreshold
                firstTime = False
            else:
                finalImage = np.concatenate((finalImage, visHorizontalImage), axis=0)
                finalThreshold = np.concatenate((finalThreshold, visHorizontalThreshold), axis=0)

            visHorizontalImage = dst
            visHorizontalThreshold = dstThreshold

        # Not changing line
        else:
            visHorizontalImage = np.concatenate((visHorizontalImage, dst), axis=1)
            visHorizontalThreshold = np.concatenate((visHorizontalThreshold, dstThreshold), axis=1)


    # Obtaining contours
    _, contours, hierarchy = cv2.findContours(finalThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Deleting erroneous contours
    contours = Preprocessing.deleteContours(contours, heightThreshold, areaThreshold)

    # Order contours by centroid left-top to bottom-right
    contours = sorted(contours, cmp=compareContours)

    # Print the angle in each sample
    finalImage = drawAngle(finalImage,contours)
    
    # Print in a file the angle of each sample
    printResults(contours)
    
    # Utilities.printContours1by1(contours, finalImage)

    # cv2.imshow("image", finalImage)
    cv2.imshow("threshold", finalImage)
    cv2.waitKey()
    # Problems when I use threshold image
    inverseThreshold = cv2.bitwise_not(finalThreshold)
    cv2.imwrite(imgOut,inverseThreshold)



def printResults(contours):
    print 'len = ', len(contours)
    listResults = []
    for i in range(0,len(contours)):
        listResults.append(i*gradeStep)
    
    listResults = np.array(listResults, np.int32)
    listResults = listResults.reshape(listResults.size, 1)

    # Saving results
    np.savetxt('MachineLearning/AngleTraining/angles.data', listResults)

def compareContours(cnt1, cnt2):
    x, y, w, h = cv2.boundingRect(cnt1)
    cx1 = x + w / 2
    cy1 = y + h / 2
    x, y, w, h = cv2.boundingRect(cnt2)
    cx2 = x + w / 2
    cy2 = y + h / 2

    # Estamos columnas diferentes
    if (cy1 + heightThreshold >= cy2):
        # Ordenamos de izquierda a dereche
        if (cx1 >= cx2):
            return 1
    return -1

def drawAngle(img,contours):
    centroidList = Preprocessing.obtainCentroid(contours)
    imgClone = np.copy(img)
    for i, cnt in enumerate(contours):
        # drawLine(imgClone,cnt)
        angle = obtainAngle(cnt,imgClone)
        cv2.putText(imgClone, str(int(angle)), (int(centroidList[i][0]), int(centroidList[i][1])), font, fontSize, colour, 2, cv2.LINE_AA)

    return imgClone

def obtainAngle(cnt,imgClone):
    point1, point2, point3, point4 = obtainPoints(cnt)

    cv2.line(imgClone, point1, point2, (0, 255, 0), 2)
    cv2.line(imgClone, point3, point4, (0, 255, 255), 2)

    angle = calculateAngle(point1, point2, point3, point4)
    if angle < 0:
        angle = angle + 180
    return angle

def obtainPoints(cnt):
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

    x, y, w, h = cv2.boundingRect(cnt)
    cx = int (x + w / 2)
    cy = int (y + h / 2)

    if(obtainDistance(leftmost,rightmost) > obtainDistance(topmost,bottommost)):
        return leftmost,rightmost,(cx,cy),(cx,topmost[1])

    else:
        return topmost,bottommost,(cx,cy),(cx,topmost[1])

def obtainDistance(point1,point2):
    xa = point1[0]
    ya = point1[1]

    xb = point2[0]
    yb = point2[1]

    distance = math.sqrt((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb))
    return distance

def calculateAngle(point1,point2,point3,point4):
    if(point2[0]-point1[0]==0):
        m1 = 100000000
    else:
        m1 = (point2[1]-point1[1])/(point2[0]-point1[0])

    if (point4[0]-point3[0] == 0):
        m2 = 100000000
    else:
        m2 = (point4[1]-point3[1])/(point4[0]-point3[0])
    angle = math.atan((m2-m1)/(1+m1*m2))
    angle = math.degrees(angle)
    return angle