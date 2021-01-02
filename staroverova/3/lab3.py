#подключаем библиотеку OpenCV
import cv2

# Загружаем каскады для лица
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Загружаем каскады для глаз
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#Загружаем каскады для улыбки
smileCascade = cv2.CascadeClassifier('haarcascade_smile.xml')

#подключаем изображение на котором будем искать фрагменты
img = cv2.imread('image.jpg')

#Переводим изображение в серый цвет
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#поиск лица
faces = faceCascade.detectMultiScale(
        gray,               
        scaleFactor=1.2,    
        minNeighbors=5,     
        minSize=(20, 20)    
    )

#поиск глаз
eyes = eyeCascade.detectMultiScale(
        gray,              
        scaleFactor=1.2,   
        minNeighbors=20,
        minSize=(5, 5),
    )

#поиск улыбки
smiles  = smileCascade.detectMultiScale(
    gray,
    scaleFactor = 1.8,
    minNeighbors = 20
    )

for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(img, (sx, sy), ((sx + sw), (sy + sh)), (0, 255,0), 5)

for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

cv2.imshow("camera", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
