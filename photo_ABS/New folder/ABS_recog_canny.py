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
# for i,file in enumerate(files):
# 	img = cv2.imread(file,1)

# 	cv2.imshow("source"+str(i),img)
print (files)
img = cv2.imread(files[0],1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

edge = cv2.Canny(gray, 15, 120)
auto = auto_canny(blurred) 

ret,thresh = cv2.threshold(gray,127,255,0)

kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(thresh,kernel,iterations = 1)

ret,cnts, _ = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_new = []
for cnt in cnts:
	# print(cv2.contourArea(cnt))
	if 20000 > cv2.contourArea(cnt) > 10000 :
		cv2.drawContours(img, cnt, -1, (0,255,0), 3)

		x,y,w,h = cv2.boundingRect(cnt)
		aspect_ratio = float(w)/h	
		print (aspect_ratio)
		if 2 > aspect_ratio > 1:	
			cnts_new.append(cnt)

font = cv2.FONT_HERSHEY_SIMPLEX
if len(cnts_new) != 0:
	msg = "WARNING " +str(len(cnts_new))+" ECUs" 
else:
	msg = "Empty box"
cv2.putText(img,msg,(int(img.shape[0]/2)-200,int(img.shape[1]/2)), font, 2,(0,0,255),4,cv2.LINE_AA)

# cv2.imshow("auto",auto)
# cv2.imshow("my",edge)
# cv2.imshow("gray",gray)
# cv2.imshow("thresh",thresh)
cv2.imshow("erodion",erosion)
cv2.imshow("source",img )
cv2.waitKey()
cv2.destroyAllWindows()