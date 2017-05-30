from __future__ import division

import os

import cv2

from MachineLearning.extractor import Extractor
from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector
from SymbolsProcessing.angleDetector import AngleDetector
from SymbolsProcessing.classifyCandidates import ClasifyCandidates
from SymbolsProcessing.extract_characteristics import ExtractCharacteristics
from SymbolsProcessing.generate_candidates import GenerateCandidates
from SymbolsProcessing.obtainROICharacters import ObtainROICharacters
from SymbolsProcessing.processROICharacter import ProcessROICharacter
from SymbolsProcessing.refinate_decission import RefinateDecission
from Utilities import utility as aux
from Utilities.createSampleImages import createSamples, drawAngle
from Utilities.preprocessing import Preprocessing




from Utilities.utility import sayIt


def cascadeVideoCamera():
    cap = cv2.VideoCapture(0)
    number = 0
    while 1:
        ret, img = cap.read()

        cv2.imshow('img', img)

        key = cv2.waitKey(1)
        # currentResults(imgParameter=img)
        if key == ord('p'):
            currentResults(imgParameter = img)
            number += 1
            cv2.imwrite('Captures/img_' + str(number) + '.jpg', img)
            print 'Imprimiendo captura ' + 'img_' + str(number) + '.jpg'

        if key == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return




def currentResults(imgParameter = None,imgPath = None):
    print 'Executing current results'
    if(imgPath is not None):
        # Preprocessing image
        img, gray, threshold, contours = Preprocessing.preprocessingImage(imgPath)
        img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        imgParameter = img

    if(imgParameter is not None):
        img, gray, threshold, contours = Preprocessing.preprocessingImageFromROI(imgParameter)
    else:
        print 'Error en el paso de parametros'
        return -1


    # imgCopy= drawAngle(img,contours)
    # cv2.imshow("imgCopy",threshold)
    # cv2.waitKey()

    # Generate candidates
    generateCandidates = GenerateCandidates()
    img, listROIs, listThreshold,listContours, listOffSetX, listOffSetY = generateCandidates.generateCandidates(img,threshold,contours)



    # for cnt in listContours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)



    # cv2.imshow("contours", img)
    # cv2.waitKey()

    # Extract characteristics
    extractCharacteristics = ExtractCharacteristics()
    listSamples = extractCharacteristics.extractCharacteristics(listROIs,listThreshold,listContours, listOffSetX, listOffSetY)

    # Classifier
    classifier = ClasifyCandidates()
    listSamples = classifier.clasifyCandidates(img,listSamples)

    # # # Refinate decission
    # refinateDecission = RefinateDecission()
    # listSamples = refinateDecission.refinateDecission(listSamples)

    # Obtain angle
    angleDetector = AngleDetector()
    listSamples =  angleDetector.obtainAngle(img,listSamples)


    # # # # # Obtain roi number
    obtainROICharacters = ObtainROICharacters()
    listSamples = obtainROICharacters.getROICharacter(img, threshold, listSamples)
    # #
    # Process roi number
    processROICharacter = ProcessROICharacter()
    listSamples = processROICharacter.processROICharacter(listSamples)

    for sample in listSamples:
        if (imgParameter is not None):
            img = imgParameter
        cv2.putText(img, sample.stringResult, (sample.offSetX, sample.offSetY), aux.font, aux.size*1.25, aux.colour, 2,cv2.LINE_AA)
        # cv2.putText(img, str(sample.angle), (sample.offSetX, sample.offSetY), aux.font, aux.size * 1.5, aux.colour, 2,cv2.LINE_AA)
        # cv2.putText(img, sample.Character, (sample.offSetX, sample.offSetY), aux.font, aux.size, aux.colour, 2,cv2.LINE_AA)

    cv2.imshow('testSample',img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # for sample in listSamples:
    #     sayIt(sample)

currentResults(imgPath='CardImages/5-diamonds-15-degrees.jpg')

i = 0
for i in range(0,17):
    print i
    currentResults(imgPath='CardImages/test'+str(i)+'.jpg')

# cascadeVideoCamera()

# Utilities.preprocessingImage("CardImages/all_spades_together.jpg")

# createSamples('SampleImages/sample_hearts.jpg','MachineLearning/AngleTraining/hearts-30.jpg')

# roiDetector = RoiDetector(heightThreshold=20,areaThreshold=50)
# extractor = Extractor()
# extractor.pixelClassifier(roiDetector, 'MachineLearning/AngleTraining/hearts-30.jpg')
#
# knn = knearest('MachineLearning/TrainingData/samples.data','MachineLearning/TrainingData/responses.data')
# knn.applyKnearest(roiDetector,'MachineLearning/CharacterTraining/set-4.png')


