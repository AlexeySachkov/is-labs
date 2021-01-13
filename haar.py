import cv2

img = cv2.imread('img3.jpg')
cv2.imshow('input', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
for (x,y,w,h) in faces:
   cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
for (ex,ey,ew,eh) in eyes:
   cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
smile = smile_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=45, minSize=(7, 7))
for (sx,sy,sw,sh) in smile:
   cv2.rectangle(img,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)

cv2.imshow('out', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
