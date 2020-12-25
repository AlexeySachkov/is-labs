```
#для распознавания элементов изображения используется каскад Хаара, для реализации подключаем opencv

import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)


    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )

    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=20,
        minSize=(5, 5),
    )
   
    smiles = smileCascade.detectMultiScale(
        gray,
        scaleFactor=1.8,
        minSize=(3, 3),
        minNeighbors=15
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    for (sx, sy, sw, sh) in smiles:
        cv2.rectangle(img, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 5)

    cv2.imshow("img", img)
    cv2.waitKey(5)

cap.release()
cv2.destroyAllWindows()
```
