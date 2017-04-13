from __future__ import division
import cv2
import numpy as np
import aux as aux


# Pass cross-image with the dimensions of the bounding rectangle that fit the contour
def matchShapeSpade(img):

    img = cv2.imread('Images/fives-1.jpg')

    # Drawing the contours in the sampleImg
    sampleImg = cv2.imread('PositiveSamples/samples.jpg')
    sampleImgBlack = aux.changeRedToBlack(sampleImg)
    cnts_sample = aux.obtainContours(sampleImgBlack)
    cnts_sample = cnts_sample[:-1]
    cv2.drawContours(sampleImg, cnts_sample, -1, (0, 255, 255), 2)

    # Label the contours
    symbols = ['diamond', 'heart', 'spades', 'clubs']
    listX,listY = aux.extractCentroid(cnts_sample)
    for j,x in enumerate(listX):
        x = listX[j]
        y = listY[j]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(sampleImg, str(j), (x,y), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)

    # Obtain the width of every contour in the sample
    listWidthSamples = []
    for cnt in cnts_sample:
        x1, y1, w1, h1 = cv2.boundingRect(cnt)
        listWidthSamples.append(w1)


   # Section img
    img = cv2.resize(img, (0, 0), fx=1, fy=1)
    imgBlack = aux.changeRedToBlack(img)
    cntsImg = aux.obtainContours(imgBlack)


    # Controlar cuantos contornos analizamos y pintamos
    cntsImg = cntsImg[:-1]
    print 'Analizando ' + str(len(cntsImg)) + ' contours '
    #cv2.drawContours(img, cntsImg, -1, (0, 255, 255), 2)


    # Obtain the width of every contour in the image
    listWidthImg = []
    for cnt in cntsImg:
        x1, y1, w1, h1 = cv2.boundingRect(cnt)
        listWidthImg.append(w1)

    cntsImgScale = np.copy(cntsImg)

    # Reescale contours of img  0.0109097039178
    for j in range(len(cntsImgScale)):
        scaleX = listWidthSamples[0] / listWidthImg[j]
        cntsImgScale[j] = scaleX * np.array(cntsImg[j])
        cntsImgScale[j] = cntsImgScale[j].astype(int)



    print 'Analisis con escala...'
    for i in range (len(cntsImgScale)):
        threshold = 0.15
        position = -1
        cx,cy = -1,-1
        for j in range (len(cnts_sample)):
            ret = cv2.matchShapes(cnts_sample[j], cntsImg[i], 1, 0.0)
            if(ret<threshold):
                position = j
                threshold = ret
                cx, cy = aux.extractSingleCentroid(cntsImg[i])
                cv2.drawContours(img, cntsImg[i], -1, (0, 255, 255), 2)

        if (position != -1):
            print 'Detectamos ' + symbols[position]
            cv2.putText(img, symbols[position], (cx, cy), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)
            # print j,ret

    cv2.imshow('image', sampleImg)
    cv2.imshow('imgToCompare', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 1

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
    watch_cascade = cv2.CascadeClassifier('Cascades/cascade-15-spades.xml')
    number = 1

    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cascade detection
        cards = watch_cascade.detectMultiScale(gray, 1.05, 40)

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

    card_cascade = cv2.CascadeClassifier('Cascades/cascade-15-spades.xml')
    img = cv2.imread('Images/fives-1.jpg')

    cv2.namedWindow('image')

    #list = ['R','G','B']
   # aux.createTrackbars(list,'image')

    img2 = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cards = card_cascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 6)

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


def test():

    imagePath = 'Images/2-hearts1.jpg'
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')

    original = cv2.imread(imagePath)


    list = ['minNeighbors','scaleFactor','B']

    aux.createTrackbars(list,'image',30)
    minNeighbors = 30
    scaleFactor = 1.05
    number = 0
    while (1):
        img = cv2.imread(imagePath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aux.changeRedToBlack(img)
        cards = card_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
        for (x, y, w, h) in cards:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            aux.drawContoursDetected(img,x,y,w,h)
        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break

        if k == ord('p'):
            number+=1
            x, y, w, h = cards[0]
            cv2.imwrite('Captures/img_' + str(number) + '.jpg', original[y:y+h,x:x+w])
            print 'Imprimiendo captura ' + 'img_' + str(number) + '.jpg'
        # get current positions of four trackbars
        minNeighbors = 1+cv2.getTrackbarPos('minNeighbors', 'image')

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()


#aux.rgbTest()
#aux.helloworld()
# matchShapes()
#a=2
# matchShapeSpade(a)
#cascadeFunction()
#cascadeVideoCamera()
#test()
matchShapeSpade(cv2.imread('Captures/img_1.jpg'))



