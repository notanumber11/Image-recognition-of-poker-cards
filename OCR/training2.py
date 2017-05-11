import sys

import numpy as np
import cv2

im = cv2.imread('/home/notanumber/Desktop/workspacePython/Tutorial/OCR/ImagesCharacters/example_training.png')
im3 = im.copy()

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
## added code
ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
cv2.imshow("sample",thresh)
cv2.waitKey()
###
#################      Now finding Contours         ###################

_,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,81)]
for cnt in contours:
    if cv2.contourArea(cnt)>50:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  h>28:
            img2 = im.copy()
            # cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.drawContours(img2, cnt, -1, (0, 0, 255), 2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('norm',img2)
            key = cv2.waitKey(0)
            print 'La tecla es ', key
            if key == 27:  # (escape to quit)
                sys.exit()
            elif key in keys:
                responses.append(key)
                sample = roismall.reshape((1,100))
                samples = np.append(samples,sample,0)

responses = np.array(responses,np.int32)
responses = responses.reshape((responses.size,1))
print "training complete"

np.savetxt('example_test_samples.data',samples)
np.savetxt('example_test_responses.data',responses)

