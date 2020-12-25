import cv2

# Программа определяет по запущенному прямому видеопотоку с веб-камеры, есть ли в кадре люди, лицо, открытые глаза

# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_lefteye_2splits.xml
left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_fullbody.xml
classifier = cv2.CascadeClassifier('haarcascade_fullbody.xml')

vid_cap = cv2.VideoCapture(0)

while True:
    ret, vid = vid_cap.read()
    gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    # frame = cv2.resize(vid, (640, 360))
    persons_detected = classifier.detectMultiScale(gray)

    # Check if people were detected on the frame
    for (p, a, s, d) in persons_detected:
        cv2.rectangle(vid, (p, a), (p + s, a + d), (255, 0, 0), 2)
        cv2.imshow('Video footage', vid)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Check if faces were detected
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (255, 0, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = vid[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        left_eye = left_eye_cascade.detectMultiScale(roi_gray)
    # Check if open eyes were detected
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)
    # Check if open left eyes were detected
            for (ix, iy, iw, ih) in left_eye:
                cv2.rectangle(roi_gray, (ix, iy), (ix + iw, iy + ih), (0, 148, 12), 3)

            def getleftmosteye(left_eye):
                leftmost = 9999999
                leftmostindex = -1
                for i in range(0, 2):
                    if left_eye[i][0] < leftmost:
                        leftmost = left_eye[i][0]
                        leftmostindex = i
                return left_eye[leftmostindex]

    cv2.imshow('vid', vid)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q') or k == 27:
        break

vid_cap.release()
cv2.destroyAllWindows()
