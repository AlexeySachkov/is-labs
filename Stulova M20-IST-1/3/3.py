import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier(r'D:\haarcascade_frontalcatface.xml')

img = cv2.imread(r'D:\cat.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray,1.1,5)

for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
 
    
cv2.startWindowThread()
cv2.imshow('Cat face',img)
cv2.waitKey(0)
cv2.destroyAllWindows()