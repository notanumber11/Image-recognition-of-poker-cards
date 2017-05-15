from __future__ import division

import sys
import numpy as np
import cv2
from Preprocessing.Preprocessing import Preprocessing

# Variables for training
# Size of the descriptor
sizeSample = 100
# Width and height ( width by height should equals shapeSample )
shapeSample = (10, 10)
# Keys range accepted from the keyboard
keys = [i for i in range(48, 81)]
# height threhold
heightThreshold = 50
areaThreshold = 200

def extractPixelCharacteristics(imgPath, labelPath = None):
    # Init variables
    samples = np.empty((0, sizeSample))
    responses = []

    # Check if we are using keyboard or file to label the data
    if(labelPath==None):
        keyboard = True
    else:
        keyboard = False
        responses = np.loadtxt(labelPath, np.float32)
        responses = responses.reshape(responses.size, 1)

    # Preprocessing image
    im, gray, thresh, contours = Preprocessing.preprocessingImage(imgPath)
    contours = sorted(contours, cmp=compareContours)

    # Showing thesholding
    cv2.imshow("sample", thresh)
    cv2.waitKey()

    # Loop contours
    for i,cnt in enumerate(contours):
        if cv2.contourArea(cnt) > areaThreshold:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > heightThreshold and h < heightThreshold * 4:
                # Preprocessing image
                imgCopy = im.copy()
                cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.drawContours(imgCopy, cnt, -1, (0, 0, 255), 2)

                diffY = (int)(0.1*h)
                diffX = (int)(0.1*w)
                h = h + diffY*2
                w = w + diffX*2

                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, shapeSample)

                cv2.imshow(',meh', roismall)
                cv2.waitKey()

                roismall = roismall.reshape((1, sizeSample))

                # Sampling with keyboard
                if keyboard:
                    key = getKey(imgCopy)
                    print 'La tecla es ', key
                    if key == 27:  # (escape to quit)
                        sys.exit()
                    elif key in keys:
                        responses.append(key)
                        samples = np.append(samples, roismall, 0)
                else:
                    sample = roismall.reshape((1, sizeSample))
                    samples = np.append(samples, sample, 0)

    # Put data in the right format when using keyboard
    if keyboard:
        responses = np.array(responses, np.int32)
        responses = responses.reshape(responses.size, 1)

    # Finish training and saving results
    print "training complete"
    np.savetxt('OCR/TrainingData/samples.data', samples)
    np.savetxt('OCR/TrainingData/responses.data', responses)

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

def getKey(imgCopy):
    cv2.imshow('imgCopy', imgCopy)
    key = cv2.waitKey(0)
    return key
