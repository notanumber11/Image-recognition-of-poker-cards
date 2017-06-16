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


def testKNN():
    roiDetector = RoiDetector(heightThreshold=20,areaThreshold=50)
    extractor = Extractor()
    extractor.pixelClassifier(roiDetector, 'MachineLearning/AngleTraining/hearts-30.jpg')
    knn = knearest('MachineLearning/TrainingData/samples.data','MachineLearning/TrainingData/responses.data')
    knn.applyKnearest(roiDetector,'MachineLearning/CharacterTraining/set-4.png')


def currentResults(imgParameter = None,imgPath = None):
    print 'Executing current results'
    if(imgPath is not None):
        # Preprocessing image
        img, gray, threshold, contours = Preprocessing.preprocessingImage(imgPath)
        # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        # imgParameter = img

    elif(imgParameter is not None):
        img, gray, threshold, contours = Preprocessing.preprocessingImageFromROI(imgParameter)
    else:
        print 'Error en el paso de parametros'
        return -1



    # Generate candidates
    generateCandidates = GenerateCandidates()
    img, listROIs, listThreshold,listContours, listOffSetX, listOffSetY = generateCandidates.generateCandidates(img,threshold,contours)

    # cv2.drawContours(img, listContours, -1, (0, 255, 255), 2)
    # cv2.imshow("meh2",img)
    # cv2.waitKey()

    # Extract characteristics
    extractCharacteristics = ExtractCharacteristics()
    listSamples = extractCharacteristics.extractCharacteristics(listROIs,listThreshold,listContours, listOffSetX, listOffSetY)

    # Classifier
    classifier = ClasifyCandidates()
    listSamples = classifier.clasifyCandidates(img,listSamples)

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

        if sample.angle < 90 or sample.angle > 270:
            cv2.putText(img, sample.stringResult, (sample.offSetX-int(sample.w/4), sample.offSetY + sample.h*2), aux.font, aux.size*1.25, aux.colour, 2,cv2.LINE_AA)
        else:
            cv2.putText(img, sample.stringResult, (sample.offSetX-int(sample.w/4), sample.offSetY - int(sample.h/6)), aux.font, aux.size*1.25, aux.colour, 2,cv2.LINE_AA)
        # cv2.putText(img, str(sample.angle), (sample.offSetX, sample.offSetY), aux.font, aux.size * 1.5, aux.colour, 2,cv2.LINE_AA)
        # cv2.putText(img, sample.Character, (sample.offSetX, sample.offSetY), aux.font, aux.size, aux.colour, 2,cv2.LINE_AA)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    cv2.imshow('testSample',img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return img

# currentResults(imgPath='CardImages/test0.jpg')

i = 1
for i in range(30,32):
    img = currentResults(imgPath='CardImages/OverallTest/test'+str(i)+'.jpg')
    cv2.imwrite('result-'+str(i)+'.jpg',img)


# createSamples('SampleImages/sample_hearts.jpg','MachineLearning/AngleTraining/hearts-30.jpg')



