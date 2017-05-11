import cv2
import numpy as np

from Preprocessing.Preprocessing import Preprocessing

# Variables for training
# Size of the descriptor
sizeSample = 100
# Width and height ( width by height should equals shapeSample )
shapeSample = (10, 10)
# Keys range accepted from the keyboard
keys = [i for i in range(48, 81)]
# height threhold
heightThreshold = 100
areaThreshold = 200

def compareContours(cnt1, cnt2):
    x, y, w, h = cv2.boundingRect(cnt1)
    cx1 = x + w / 2
    cy1 = y + h / 2
    x, y, w, h = cv2.boundingRect(cnt2)
    cx2 = x + w / 2
    cy2 = y + h / 2

    # we are in different columns ( sort top to bottom )
    if (cy1 + heightThreshold >= cy2):
        # Sort from left to right
        if (cx1 >= cx2):
            return 1
    return -1

def checkResults(pathResponses, results):
    # Load corrects results from file
    responses = np.loadtxt(pathResponses, np.float32)
    responses = responses.reshape((1, responses.size))

    # Change format results
    results = np.array(results, np.int32)
    results = results.reshape((1,results.size))

    # Checking if the lenght is the same
    if results.size != responses.size:
        print 'Error en el numero de muestras detectadas'
        return

    diff = np.subtract(responses, results)
    # print responses
    # print results
    print np.sum(diff)

def trainingKnearest():
    samples = np.loadtxt('OCR/TrainingData/samples.data',np.float32)
    responses = np.loadtxt('OCR/TrainingData/responses.data',np.float32)
    responses = responses.reshape((responses.size,1))
    knn = cv2.ml.KNearest_create()
    knn.train(samples,cv2.ml.ROW_SAMPLE,responses)
    return knn

def applyKnearest(imgPath):
    knn = trainingKnearest()
    # preprocessing image
    img, gray, thresh, contours = Preprocessing.preprocessingImage(imgPath)
    # sort contours from upper-left to bottom-right
    contours = sorted(contours, cmp=compareContours)

    out = np.zeros(img.shape, np.uint8)
    cv2.imshow("thresh",thresh)
    cv2.waitKey()

    resultsTesting = []

    # Find the right position to apply k-nearest
    for cnt in contours:
        if cv2.contourArea(cnt)>areaThreshold:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  h>heightThreshold and h < heightThreshold * 4:
                # Preprocessing image
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,shapeSample)
                roismall = roismall.reshape((1,sizeSample))
                roismall = np.float32(roismall)

                # Applying algorithm knearest
                retval, results, neigh_resp, dists = knn.findNearest(roismall, k = 1)
                string = str(((results[0][0])))
                cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

                # Save results for testing
                resultsTesting.append(results[0][0])

    # Save results when they are 100% Ok
    # np.savetxt('TextResults/example_test.txt',resultsTesting)

    print "knearest complete"

    # cv2.imshow('im', img)
    cv2.imshow('out',out)
    cv2.waitKey(0)
    # checkResults('TextResults/example_test.txt',resultsTesting)

# applyKnearest('ImagesCharacters/example_training.png')