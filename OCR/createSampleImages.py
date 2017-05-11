import cv2
import numpy as np

samplesPerLine = 10
numberOfSamples = 60
gradeStep = 360/numberOfSamples
heightThreshold = 100
areaThreshold = 200

font = cv2.FONT_HERSHEY_SIMPLEX
colour = (0, 255, 255)

def create360samples(imgpath):

    if(numberOfSamples%samplesPerLine):
        print 'Error: samples per line and number of samples should be multiple'
        return

    if (360 % gradeStep):
        print 'Error: 360 and number of samples should be multiple'
        return

    print 'Number of samples ', numberOfSamples
    print 'Grade step ', gradeStep

    img = cv2.imread(imgpath)
    rowsGlobal, colsGlobal,_ = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
    ret2, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    visHorizontalImage = img
    visHorizontalThreshold = threshold
    firstTime = True

    for i in range (1, numberOfSamples+1):
        M = cv2.getRotationMatrix2D((colsGlobal / 2, rowsGlobal / 2), i*gradeStep, 1)
        dst = cv2.warpAffine(img, M, (colsGlobal, rowsGlobal))
        dstThreshold = cv2.warpAffine(threshold, M, (colsGlobal, rowsGlobal))

        # Cambio de linea
        if(i%(samplesPerLine) == 0):
            if (firstTime):
                finalImage = visHorizontalImage
                finalThreshold = visHorizontalThreshold
                firstTime = False
            else:
                finalImage = np.concatenate((finalImage,visHorizontalImage),axis = 0)
                finalThreshold = np.concatenate((finalThreshold, visHorizontalThreshold), axis=0)

            visHorizontalImage = dst
            visHorizontalThreshold = dstThreshold

        else:
            visHorizontalImage = np.concatenate((visHorizontalImage, dst), axis=1)
            visHorizontalThreshold = np.concatenate((visHorizontalThreshold, dstThreshold), axis=1)

    # cv2.imwrite("supersample.jpg",finalImage)

    _, contours, hierarchy = cv2.findContours(finalThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    contours = deleteContours(contours,heightThreshold,areaThreshold)

    contours = sorted(contours,cmp = compareContours)
    centroidList = obtainCentroid(contours)

    for i,cnt in enumerate(contours):
        cv2.putText(finalImage, str(i*gradeStep), (centroidList[i][0],centroidList[i][1]), font, 0.8, colour, 2,cv2.LINE_AA)

    # printContours1by1(contours, finalImage)

    cv2.imshow("image", finalImage)
    cv2.waitKey()


def deleteContours(contours,height,area):
    deleteList = []
    for i in range(0, (len(contours))):
        x, y, w, h = cv2.boundingRect(contours[i])
        # print h
        if (h < height or h > 2*height):
            deleteList.append(i)


    contoursFiltered = np.delete(contours, deleteList, axis=0)
    # print 'Lenght ', len(contours)
    return contoursFiltered

def printContours1by1(contours, finalImage):
    print "Drawing contours = ",len(contours)
    for cnt in contours:
        img2 = np.copy(finalImage)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.drawContours(img2, cnt, -1, (0, 0, 255), 2)
        cv2.imshow("image", img2)
        cv2.waitKey()

def obtainCentroid(cnts):
    centroidList = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cx = x + w/2
        cy = y + h/2
        # print cx,cy
        centroidList.append([cx,cy])
    return centroidList

def compareContours(cnt1,cnt2):

    x, y, w, h = cv2.boundingRect(cnt1)
    cx1 = x + w / 2
    cy1 = y + h / 2

    x, y, w, h = cv2.boundingRect(cnt2)
    cx2 = x + w / 2
    cy2 = y + h / 2

    # print cx1,cy1
    # print cx2,cy2

    # Estamos columnas diferentes
    if (cy1 + heightThreshold >= cy2):
        # Ordenamos de izquierda a dereche
        if(cx1 >= cx2):
            return 1


    return -1



