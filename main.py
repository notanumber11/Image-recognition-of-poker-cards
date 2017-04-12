from __future__ import division
import cv2
import numpy as np
import aux as aux


# Pass cross-image with the dimensions of the bounding rectangle that fit the contour
def matchShapeSpade(imgToCompare):

    # Preparing the contour of the spades sample
    img1 = cv2.imread('PositiveSamples/sample_spades.jpg')
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    img1_2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    spadesContour = contours[1]

    # Obtain the minimun rectangle that fits the contours of the spades sample
    x1, y1, w1, h1 = cv2.boundingRect(spadesContour)

    # Obtain the shape of the rectangle image
    h2, w2, m = imgToCompare.shape

    scaleX = w1/w2

    scaleY = h1/h2


    # Scale image
    imgToCompare = cv2.resize(imgToCompare, None, fx = scaleX, fy=scaleY, interpolation=cv2.INTER_CUBIC)

    imgToCompare = 255 - imgToCompare
    contourToCompare = aux.drawAllContours(imgToCompare)


    ret = 1
    if(len(contourToCompare)>0):
        contourToCompare = contourToCompare[0]
        ret = cv2.matchShapes(spadesContour, contourToCompare, 1, 0.0)
        if(ret<0.1):
            print 'Es una espada con ret ' + str(ret)
            cv2.imshow('imgToCompare',imgToCompare)
            cv2.waitKey(0)
    cv2.destroyAllWindows()

    return ret

def matchShapes():
    img1 = cv2.imread('PositiveSamples/sample_spades.jpg')

    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
    img1_2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    cv2.drawContours(img1, contours, 1, (0, 255, 255), 2)

    
    img2 = cv2.imread('PositiveSamples/sample_spades.jpg')

    # Rotate 90
    # rows, cols , m = img2.shape
    # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 180, 1)
    # dst = cv2.warpAffine(img2, M, (cols, rows))
    #
    # img2 = dst


    # Scale image
    res = cv2.resize(img2, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    img2 = res

    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(gray2, (1, 1), 1000)
    flag2, thresh2 = cv2.threshold(blur2, 120, 255, cv2.THRESH_BINARY)
    img2_1, contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    cv2.drawContours(img2, contours2, 1, (0, 255, 255), 2)

    cv2.imshow('img1', img1)
    cv2.imshow('img2', img2)


    ret = 0
    ret = cv2.matchShapes(contours2[1], contours[1], 1, 0.0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print ret


def detectCircles():
    img = cv2.imread('Images/fives-3.jpg')
    img = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


    list = ['dp','minDist','param1','param2']
    aux.createTrackbars(list,'img')



    # Circle detection
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=0, maxRadius=100)
    if circles.size > 0:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)


    # Showing image

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cascadeVideoCamera():
    cap = cv2.VideoCapture(0)
    watch_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')
    number = 1
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cascade detection
        cards = watch_cascade.detectMultiScale(gray, 1.05, 200)

        # process regions with the card detection
        for (x, y, w, h) in cards:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            # contour = aux.drawContoursDetected(img,gray,x,y,w,h)
            #
            # # Draw rectangle in the contour
            # x1, y1, w1, h1 = cv2.boundingRect(contour)
            # x1 = x+x1
            # y1 = y +y1
            # cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            #
            # # The rectangle image with the contour
            # crop_img = img[y1:y1 + h1, x1:x1 + w1]





        # show the results
        cv2.imshow('img', img)

        key = cv2.waitKey(1)

        if key == ord('p'):
            number +=1
            cv2.imwrite('Captures/img_'+ str(number)+'.jpg',img)
            print 'Imprimiendo captura ' + 'img_' + str(number) +'.jpg'

        if key == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return

def cascadeFunction():
    print 'Executing...'

    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')
    img = cv2.imread('Images/fives-1.jpg')

    cv2.namedWindow('image')

    #list = ['R','G','B']
   # aux.createTrackbars(list,'image')

    img2 = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cards = card_cascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 200)

    numOfSpades = 0
    for (x, y, w, h) in cards:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        # Obtain the contours that are inside of the cascade detection
        contours = aux.drawContoursDetected(img, gray, x, y, w, h)

        # Obtain the rectangles that contain that contours
        # rectangles = aux.drawContourRectangle(contours,img,x,y)
        # print 'El tamano del rectangulo es ' + str(len(rectangles))
        # for i,rectangle in enumerate(rectangles):
        #     print 'Rectangle en cascada ',i ,rectangle.x, rectangle.y
        #     crop_img = img2[rectangle.y:rectangle.y + rectangle.h, rectangle.x:rectangle.x + rectangle.w]
            # cv2.imshow('cropImage',crop_img)
            # cv2.waitKey(0)
    #         ret = matchShapeSpade(crop_img)
    #
    #         if (ret < 0.1):
    #             numOfSpades+=1
    #
    # print 'El numero de espadas es ' + str(numOfSpades)


    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#aux.rgbTest()
#aux.helloworld()
# matchShapes()
a=2
# matchShapeSpade(a)
#cascadeFunction()
#cascadeVideoCamera()

def test():

    imagePath = 'Images/randomCards-1.jpg'
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')

    img = cv2.imread(imagePath)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    list = ['minNeighbors','scaleFactor','B']
    aux.createTrackbars(list,'image',30)
    minNeighbors = 30
    scaleFactor = 1.05
    while (1):
        img = cv2.imread(imagePath)
        cards = card_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
        for (x, y, w, h) in cards:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        minNeighbors = 1+cv2.getTrackbarPos('minNeighbors', 'image')

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

test()
