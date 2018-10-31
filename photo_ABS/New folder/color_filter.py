import numpy as np 
import cv2
import matplotlib.pyplot as plt	
import os

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged

files = [file for file in os.listdir() if file.endswith(".png")]
print(files)
img = cv2.imread(files[2],1)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
 
    # формируем начальный и конечный цвет фильтра
h_min = np.array((0, 0, 166), np.uint8)
h_max = np.array((86, 33, 251), np.uint8)

    # накладываем фильтр на кадр в модели HSV
thresh = cv2.inRange(hsv, h_min, h_max)

result = cv2.bitwise_and(img, img, mask=thresh)

blurred = cv2.GaussianBlur(result, (3, 3), 0)
auto = auto_canny(blurred)
    
ret,cnts, _ = cv2.findContours(auto, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in  cnts:
	area = cv2.contourArea(i)    	
	if area > 800:
		print(area)
		cv2.drawContours(img,i,-1,(0,255,0), 2)
cv2.imshow('mask', thresh) 
cv2.imshow('result2', result) 
cv2.imshow('edged', auto)
cv2.imshow("scr",img)
cv2.waitKey()


cv2.destroyAllWindows()