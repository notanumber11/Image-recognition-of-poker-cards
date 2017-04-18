import cv2
import numpy as np
import aux as rF
import matplotlib.pyplot as plt
import os
from rectangle import Rectangle


def helloworld():
    print 'hello world'
    print np.__version__
    print cv2.__version__
    return

def addNewLinesToFile(path):
    output = open('output.txt', 'w')
    with open(path) as f:
        for line in f:
            output.write(line + '\n')  # python will convert \n to os.linesep
    return


def imgToGrayScale(path):
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('normal_image',image)
    cv2.imshow('gray_image',gray_image)
    cv2.imwrite('output_grayscale.jpg', gray_image)
    return


def deleteSmallImages(pathToDirectory, widthImg, heightImg):
    externalCount = 0
    for filename in os.listdir(pathToDirectory):
        print 'numero ' + str(externalCount)
        externalCount += 1
        img1 = cv2.imread(pathToDirectory + '/' + filename)
        height, width, channels = img1.shape
        count = 0
        if heightImg > height or widthImg > width:
            print 'deleting ' + pathToDirectory + '/' + filename
            #print str(height) + ' ' +  str(width)
            os.remove(pathToDirectory + '/' + filename)
            count += 1
    print 'finish with ' + str(count)
    return


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

    print "La longitud es " ,a
    img2[mask1 == 255] = [0, 0, 0]
    img2[mask2 == 255] = [0, 0, 0]
    return img2


def fittingLine(img,cnt):
    rows, cols = img.shape[:2]
    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
    print vx,vy,x,y
    lefty = int((-x * vy / vx) + y)
    righty = int(((cols - x) * vy / vx) + y)

    incognita = (0-y)/vy
    incognita2= (rows-y)/vy
    # print lefty,righty
    # cv2.line(img, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)
    cv2.line(img, (x, incognita2), (x, incognita), (0, 255, 0), 2)


def extractCentroid(contours):
    listCX = []
    listCY = []
    # ComputerCentroid
    for contour in contours[:]:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            listCX.append(cx)
            listCY.append(cy)
    return listCX,listCY


def extractSingleCentroid(contour):
    M = cv2.moments(contour)
    cx,cy = 0,0
    if M["m00"] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    return cx,cy

def isInsideRectangle(x,y,x0,y0,w,h):
    if x>x0 and x<(x0+w):
        if y>y0 and y<(y0+h):
            return True
    return False


def drawBoundingRectangle(contours, img, offsetX, offsetY):
    print 'El tamano de los contornos es ' + str(len(contours))
    rectangles  = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x += offsetX
        y += offsetY
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rectangle = Rectangle(x,y,w,h)
        rectangles.append(rectangle)

    return rectangles


def drawMinimalRectangle(img,cnt):
    for c in cnt:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)


def drawContoursDetected(img, x, y,w,h):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    crop_img = gray_img[y:y + h, x:x + w]

    # prepare for contour detection
    blur = cv2.GaussianBlur(crop_img, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # change to 0
    contours = sorted(contours, key=cv2.contourArea)


    # draw the contours with the offset
    cv2.drawContours(img, contours[:-1], -1, (0, 255, 255), 2, offset=(x, y))

    return contours[:-1]

def drawAllContours(contours,imgDest):
    cv2.drawContours(imgDest, contours, -1, (0, 255, 255), 2)


def obtainContours(imgSrc):
    crop_img = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
    # prepare for contour detection
    blur = cv2.GaussianBlur(crop_img, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # change to 0
    contours = sorted(contours, key=cv2.contourArea)
    # print 'El tamano de los contornos es ' +str(len(contours))
    return contours

def nothing(x):
    pass

def rgbTest():
    # Create a black image, a window
    img = cv2.imread('Images/fives-1.jpg')
    cv2.namedWindow('image')

    list = ['R','G','B']
    createTrackbars(list,'image')

    # create switch for ON/OFF functionality
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'image', 0, 1, nothing)

    while (1):
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        r = cv2.getTrackbarPos('R', 'image')
        g = cv2.getTrackbarPos('G', 'image')
        b = cv2.getTrackbarPos('B', 'image')
        s = cv2.getTrackbarPos(switch, 'image')

        # if s == 0:
        #     img[:] = 0
        # else:
        #     img[:] = [b, g, r]

    cv2.destroyAllWindows()


def createTrackbars(list,imageName,initValue):
    cv2.namedWindow(imageName)
    for x in list:
        cv2.createTrackbar(x, imageName, initValue, 255, nothing)

def detectCircles():
    img = cv2.imread('Images/fives-3.jpg')
    img = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


    list = ['dp', 'minDist', 'param1', 'param2']
    aux.createTrackbars(list, 'img')

    # Circle detection
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=0,
                               maxRadius=100)
    if circles.size > 0:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Showing image

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()