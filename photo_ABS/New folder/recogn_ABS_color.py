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


def nothing(*arg):
        pass

files = [file for file in os.listdir() if file.endswith(".png")]
print(files)
img = cv2.imread(files[1],1)
cv2.namedWindow( "settings" ) # создаем окно настроек



# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 166, 255, nothing)
cv2.createTrackbar('h2', 'settings', 86, 255, nothing)
cv2.createTrackbar('s2', 'settings', 33, 255, nothing)
cv2.createTrackbar('v2', 'settings', 251, 255, nothing)





while True:
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    result = cv2.bitwise_and(img, img, mask=thresh)

    blurred = cv2.GaussianBlur(result, (3, 3), 0)
    auto = auto_canny(blurred)
    
    ret,cnts, _ = cv2.findContours(auto, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
    	if cv2.contourArea(cnt,True) >100:
    		cv2.drawContours(img,cnt,-1,(0,255,0), -1)
    	
    cv2.imshow('mask', thresh) 
    cv2.imshow('result2', result) 
    cv2.imshow('edged', auto)
    cv2.imshow("scr",img)
    ch = cv2.waitKey(5)
    if ch == 27:
    	break

cv2.destroyAllWindows()



