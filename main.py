from __future__ import division

import cv2

from Preprocessing import aux as aux
from OCR import createSampleImages as sampler
from SampleCreator import SampleCreator


def cascadeVideoCamera():
    cap = cv2.VideoCapture(0)
    watch_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')
    number = 1
    sampleCreator = SampleCreator()
    while 1:
        ret, img = cap.read()

        sampleCreator.obtainSamples(img=img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cascade detection
        cards = watch_cascade.detectMultiScale(gray, 1.05, 30)

        # process regions with the card detection
        for (x, y, w, h) in cards:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            crop_img = img[y:y+h,x:x+w]

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

def photoTest(imagePath):
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')

    original = cv2.imread(imagePath)

    list = ['minNeighbors','scaleFactor','B']

    aux.createTrackbars(list, 'image', 40)
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

def photo(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Load sample creator
    sampleCreator = SampleCreator()

    # # Run sample creator
    # img,listSamples,listOffSetX,listOffSetY = sampleCreator.obtainSamples(imagePath)
    # sampleCreator.testSamples(img,listSamples,listOffSetX,listOffSetY )

    # Load classifier
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')
    # Params classifier
    minNeighbors = 20
    scaleFactor = 1.05

    # Perform first detection with haar cascade
    cards = card_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    for (x, y, w, h) in cards:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        crop_img = img[y:y+h,x:x+w]

        # Run sample creator
        imgSample, listSamples, listOffSetX, listOffSetY = sampleCreator.obtainSamples(img=crop_img)
        # Show samples
        # sampleCreator.showSamples(listSamples)
        # Test samples
        sampleCreator.testSamples(imgSample, listSamples, listOffSetX, listOffSetY)

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # ret3, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # ret, th1 = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
    # im2, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # aux.drawAllContours(contours,img)
    cv2.imshow('image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


# img = cv2.imread("Images/randomCards-3.jpg")
# sampleCreator = SampleCreator()
# img,listSamples,listOffSetX,listOffSetY = sampleCreator.obtainSamples(img = img )
# sampleCreator.testSamples(img,listSamples,listOffSetX,listOffSetY )
# cv2.imshow('testSample',img)
# cv2.waitKey()


sampler.create360samples("SampleImages/sample_clubs.jpg")
# pre = Preprocessing()
# pre .preprocessingImage("Images/all_spades_together.jpg")


