import cv2
import numpy as np


image	= cv2.imread('image.jpg')
gray_img	=	cv2.cvtColor(image,	cv2.COLOR_BGR2GRAY)
img	= cv2.medianBlur(gray_img,	5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles	= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,120,param1=100,param2=30,minRadius=0,maxRadius=0)
circles	= np.uint16(np.around(circles))

for	i in circles[0,:]:
				cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),6)
				cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow("HoughCirlces",	image)
cv2.waitKey()
cv2.destroyAllWindows()