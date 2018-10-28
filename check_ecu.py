# Проверка изображения на наличие ECU методом 
#описывания прямоугольника вокруг каждого контура и проверки соотношения сторон
#Если все ок Описываем дополнительно поверный прямоугольник и проверяем центры
#

import numpy as np 
import cv2
import matplotlib.pyplot as plt	
# import image
img = cv2.imread("photo.png",1)

# find contours on grey splace
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(grey, 15, 120)

# NOTICE!!! RETR_EXTERNAL
ret,cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# iteration contours
for cnt in cnts:
        # use boundaring  rectangle for every contour an check aspect  ratio
		x,y,w,h = cv2.boundingRect(cnt)
		aspect_ratio = float(w)/h
		
		if 1.3 > aspect_ratio > 1.2 and w*h >5000:

			# if OK draw contour an boundaring rectangle
			cv2.drawContours(img,cnt,-1,(0,255,0), 2)
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,265),2)

			
			center_bound = (int((w/2)+x),int((h/2)+y))
			cv2.circle(img,center_bound, 2, (255,0,255), -1)

			
			
			# boundaring roteted rectangle
			rect = cv2.minAreaRect(cnt) 
			box = cv2.boxPoints(rect) 
			box = np.int0(box) # see tutorial fyi
			cv2.drawContours(img,[box],0,(255,0,0),2) # don't know about []
			

			# find center of ratated rectangle
			center = int(rect[0][0]),int(rect[0][1])
			cv2.circle(img,center, 2, (0,0,255), -1)
			
			


			# check centers on gap (x,y axises)


			if  center[0]+3 > center_bound[0] > center[0]-3 and center[1]+3 > center_bound[1] > center[1]-3 :
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(img,"OK",center, font, 2,(0,255,0),4,cv2.LINE_AA)
			else:	
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(img,"NOK",center, font, 2,(0,0,255),4,cv2.LINE_AA)


			








# cv2.imshow("scr",grey)
# cv2.imshow("edged",edged)
cv2.imshow("img",img)

cv2.waitKey()