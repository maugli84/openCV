import numpy as np
import cv2

#cap = cv2.VideoCapture('sample1.mp4')

import cv2
import numpy as np

threshold = 150000 

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

# capture image from cam
cam =cv2.VideoCapture(1)#1 -web on compuetr,0 - wifi cam from phone  
cv2.namedWindow("from cam")
ret,frame = cam.read()
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

#print (ret)
while 1:
    ret,frame = cam.read()
    cv2.namedWindow("from cam")
    cv2.imshow("from cam", diffImg(t_minus, t, t_plus) )
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus)) 
    print (totalDiff)
    if totalDiff  >=   threshold :
	    # print ('motion detected')
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"MOTION",(100,100), font, 2,(0,255,0),4,cv2.LINE_AA)
    cv2.imshow("from cam",frame)
    key = cv2.waitKey(10)
    if key ==27:
        cv2.destroyWindow("from cam")
        break		