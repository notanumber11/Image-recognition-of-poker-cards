import cv2
import numpy as np

#######   training part    ###############
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

knn = cv2.ml.KNearest_create()
knn.train(samples,cv2.ml.ROW_SAMPLE,responses)
############################# testing part  #########################

im = cv2.imread('../Images/randomCards-3.jpg')
im = cv2.imread('randomCards-3.jpg')
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)

thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh",thresh)
cv2.waitKey()

# added code
blur = cv2.GaussianBlur(gray,(5,5),0)
ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)
##
_,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt)>80:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>28:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = knn.findNearest(roismall, k = 1)
            string = str(unichr((results[0][0])))
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)