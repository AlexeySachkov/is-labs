import cv2
import os
import numpy as np



#Данная функция возвращает прямоугольник для обнаруженного лица вместе с изображением в оттенках серого
def faceDetection(test_img):
    #Преобразовать цветное изображение в оттенки серого
    gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    #Загрузка классификатора хаара
    face_haar_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #Возвращает прямоугольники
    faces=face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.32,minNeighbors=5)

    return faces,gray_img

#Данная функция возвращает часть изображения, на которой изображено лицо
def labels_for_training_data(directory):
    faces=[]
    faceID=[]

    for path,subdirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                #Пропускаем файлы, которые начинаются с точки
                print("Пропускаем системные файлы")
                continue

            #Получаем имена подпапок
            id=os.path.basename(path)
            #Получаем пути изображений
            img_path=os.path.join(path,filename)
            print("img_path:",img_path)
            print("id:",id)
            #Загрузачем каждое изображение по очереди
            test_img=cv2.imread(img_path)
            if test_img is None:
                print("Изображение загружено неправильно")
                continue
            #Вызываем функцию faceDetection для получения лиц на определенном изображении
            #Предполагаем, что загружаются изображения только одного человека
            faces_rect,gray_img=faceDetection(test_img)
            if len(faces_rect)!=1:
               continue
            (x,y,w,h)=faces_rect[0]
            #Обрезаем область лица из изображения
            roi_gray=gray_img[y:y+w,x:x+h]
            faces.append(roi_gray)
            faceID.append(int(id))
    return faces,faceID


#Данная функция обучает классификатор Хаара
def train_classifier(faces,faceID):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer

#Данная функция рисует ограничивающие рамки вокруг обнаруженного лица
def draw_rect(test_img,face):
    (x,y,w,h)=face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=5)

#Данная функция записывает имя человека для обнаруженной метки
def put_text(test_img,text,x,y):
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_DUPLEX,2,(255,0,0),4)