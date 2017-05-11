import cv2
import numpy as np

# Properties
from Preprocessing.Preprocessing import Preprocessing

samplesPerLine = 20
numberOfSamples = 360
gradeStep = 360 / numberOfSamples

# Thresholds
heightThreshold = 100
areaThreshold = 200

# Drawing variables
font = cv2.FONT_HERSHEY_SIMPLEX
colour = (0, 255, 255)
fontSize = 0.8

# Method to create samples with different angles
def createSamples(imgpath):
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
    
    # printContours1by1(contours, finalImage)

    # cv2.imshow("image", finalImage)
    # cv2.imshow("threshold", finalThreshold)
    # cv2.waitKey()
    # Problems when I use threshold image
    inverseThreshold = cv2.bitwise_not(finalThreshold)
    cv2.imwrite("OCR/ImagesSymbols/clubs.jpg",inverseThreshold)



def printResults(contours):
    listResults = []
    for i in range(0,len(contours)):
        listResults.append(i*gradeStep)
    
    listResults = np.array(listResults, np.int32)
    listResults = listResults.reshape(listResults.size, 1)

    # Saving results
    np.savetxt('OCR/ImagesSymbols/clubs_angle.txt', listResults)

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
        cv2.putText(imgClone, str(i * gradeStep), (int(centroidList[i][0]), int(centroidList[i][1])), font, fontSize, colour, 2, cv2.LINE_AA)
    return imgClone