from __future__ import division
import cv2
import numpy as np
import aux as aux


# Pass cross-image with the dimensions of the bounding rectangle that fit the contour
def matchShapeSpade(img, offsetX=0,offsetY=0,img2=None):

    #img = cv2.imread('Captures/img_2.jpg')

    # Drawing the contours in the sampleImg
    sampleImg = cv2.imread('Samples/samples.jpg')
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
            ret = cv2.matchShapes(cnts_sample[j], cntsImgScale[i], 1, 0.0)
            if(ret<threshold):
                position = j
                threshold = ret
                cx, cy = aux.extractSingleCentroid(cntsImg[i])
                cv2.drawContours(img, cntsImg[i], -1, (0, 255, 255), 2)

        if (position != -1):
            print 'Detectamos ' + symbols[position]
            if(img2!=None):
                cv2.putText(img2, symbols[position], (cx+offsetX, cy+offsetY), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(img, symbols[position], (cx+offsetX, cy+offsetY), font, 0.5, (11, 255, 255), 2, cv2.LINE_AA)
            # print j,ret

    if(img2==None):
        cv2.imshow('image', sampleImg)
        cv2.imshow('imgToCompare', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return 1


def cascadeVideoCamera():
    cap = cv2.VideoCapture(0)
    watch_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')
    number = 1

    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cascade detection
        cards = watch_cascade.detectMultiScale(gray, 1.05, 30)

        # process regions with the card detection
        for (x, y, w, h) in cards:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            crop_img = img[y:y+h,x:x+w]
            matchShapeSpade(crop_img,x,y)
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


def test():


    imagePath = 'Images/twos-1.jpg'
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')

    original = cv2.imread(imagePath)

    list = ['minNeighbors','scaleFactor','B']

    aux.createTrackbars(list,'image',40)
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
            crop_img = img[y:y+h,x:x+w]
            matchShapeSpade(crop_img,x,y,img)
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


def prueba():
    imagePath = 'Samples/sample_clubs.jpg'

    original = cv2.imread(imagePath)
    original = cv2.resize(original, (0, 0), fx=1, fy=1)

    # Rotation test
    rows, cols, m = original.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
   # original = cv2.warpAffine(original, M, (cols, rows))

    black = aux.changeRedToBlack(original)
    contours = aux.obtainContours(black)
    print len(contours)
    aux.drawAllContours(contours,original)

    # aux.drawBoundingRectangle(contours, original, 0, 0)
    # aux.drawMinimalRectangle(original,contours)
    for contour in contours[:-1]:
        aux.fittingLine(original,contour)
    cv2.imshow('test',original)
    cv2.waitKey(0)

prueba()
#cascadeVideoCamera()
#test()
#matchShapeSpade(cv2.imread('Captures/img_1.jpg'))


