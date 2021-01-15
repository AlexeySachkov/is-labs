import cv2

img = cv2.imread('face.jpg')
cv2.imshow('before', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
for (x,y,w,h) in faces:
   cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)

eyes = cv2.CascadeClassifier('haarcascade_eye.xml').detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
for (ex,ey,ew,eh) in eyes:
   cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,0,255),3)

l_eye = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml').detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
for (ex,ey,ew,eh) in l_eye:
   cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(50,100,150),3)

r_eye = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml').detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
for (ex,ey,ew,eh) in r_eye:
   cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(150,100,50),3)

smile = cv2.CascadeClassifier('haarcascade_smile.xml').detectMultiScale(gray, scaleFactor=1.3, minNeighbors=45)
for (sx,sy,sw,sh) in smile:
   cv2.rectangle(img,(sx,sy),(sx+sw,sy+sh),(0,255,),3)

cv2.imshow('after', img)
cv2.waitKey(0)
cv2.destroyAllWindows()