from __future__ import division

import cv2

from MachineLearning.extractor import Extractor
from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector
from SymbolsProcessing.angleDetector import AngleDetector
from SymbolsProcessing.classifyCandidates import ClasifyCandidates
from SymbolsProcessing.extract_characteristics import ExtractCharacteristics
from SymbolsProcessing.generate_candidates import GenerateCandidates
from SymbolsProcessing.obtainROICharacters import ObtainROICharacters
from SymbolsProcessing.refinate_decission import RefinateDecission
from Utilities import utility as aux
from Utilities.createSampleImages import createSamples, drawAngle
from Utilities.preprocessing import Preprocessing


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
            crop_img = img[y:y + h, x:x + w]

        # show the results
        cv2.imshow('img', img)

        key = cv2.waitKey(1)

        if key == ord('p'):
            number += 1
            cv2.imwrite('Captures/img_' + str(number) + '.jpg', img)
            print 'Imprimiendo captura ' + 'img_' + str(number) + '.jpg'

        if key == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return

def photoTest(imagePath):
    card_cascade = cv2.CascadeClassifier('Cascades/cascade-20-2-spades.xml')

    original = cv2.imread(imagePath)

    list = ['minNeighbors', 'scaleFactor', 'B']

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
            crop_img = img[y:y + h, x:x + w]

        cv2.imshow('image', img)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break

        if k == ord('p'):
            number += 1
            x, y, w, h = cards[0]
            cv2.imwrite('Captures/img_' + str(number) + '.jpg', original[y:y + h, x:x + w])
            print 'Imprimiendo captura ' + 'img_' + str(number) + '.jpg'
        # get current positions of four trackbars
        minNeighbors = 1 + cv2.getTrackbarPos('minNeighbors', 'image')

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
        crop_img = img[y:y + h, x:x + w]

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

def currentResults():
    # Preprocessing image
    img, gray, threshold, contours = Preprocessing.preprocessingImage('CardImages/2-spades7.jpg')

    # imgCopy= drawAngle(img,contours)
    # cv2.imshow("imgCopy",imgCopy)
    # cv2.waitKey()

    # Generate candidates
    generateCandidates = GenerateCandidates()
    img, listROIs, listThreshold,listContours, listOffSetX, listOffSetY = generateCandidates.generateCandidates(img,threshold,contours)
    # Extract characteristics
    extractCharacteristics = ExtractCharacteristics()
    listSamples = extractCharacteristics.extractCharacteristics(listROIs,listThreshold,listContours, listOffSetX, listOffSetY)

    # Classifier
    classifier = ClasifyCandidates()
    listSamples = classifier.clasifyCandidates(img,listSamples)

    # Refinate decission
    refinateDecission = RefinateDecission()
    listSamples = refinateDecission.refinateDecission(listSamples)

    # Obtain angle
    angleDetector = AngleDetector()
    listSamples =  angleDetector.obtainAngle(img,listSamples)

    # Obtain roi number
    obtainROICharacters = ObtainROICharacters()
    obtainROICharacters.obtainNumberResponse(img,listSamples)


    for sample in listSamples:
        cv2.putText(img, sample.label, (sample.offSetX, sample.offSetY), aux.font, aux.size, aux.colour, 2,cv2.LINE_AA)
        cv2.putText(sample.img, str(sample.angle), (0,int(sample.h/2)), aux.font, aux.size, aux.colour, 2,cv2.LINE_AA)

    cv2.imshow('testSample',img)
    cv2.waitKey()

currentResults()



# Utilities.preprocessingImage("CardImages/all_spades_together.jpg")

# createSamples('SampleImages/sample_hearts.jpg','MachineLearning/AngleTraining/hearts-30.jpg')

# roiDetector = RoiDetector(heightThreshold=20,areaThreshold=100)
# extractor = Extractor()
# extractor.pixelClassifier(roiDetector, 'MachineLearning/AngleTraining/spades-360.jpg','MachineLearning/AngleTraining/angles.data')
# #
# knn = knearest('MachineLearning/TrainingData/samples.data','MachineLearning/TrainingData/responses.data')
# knn.applyKnearest(roiDetector,'CardImages/2-spades7.jpg')
#
