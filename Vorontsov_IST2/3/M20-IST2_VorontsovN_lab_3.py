import time

import cv2

if __name__ == "__main__":

    eyes_cascade = cv2.CascadeClassifier("./dataset/haarcascade_eye.xml")
    for i in range(1, 29):
        photo = cv2.imread("./images/image.jpg")
        gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        start = time.time()
        scale_factor = 1.1 + 0.1 * i
        eyes = eyes_cascade.detectMultiScale(gray, scale_factor, 10)
        end = time.time()
        for (x, y, w, h) in eyes:
            photo = cv2.rectangle(photo, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(photo, str(end - start), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv2.putText(photo, "Scale factor:" + str(scale_factor), (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            roi_gray = gray[y: y + h, x: x + w]
            roi_color = photo[y: y + h, x: x + w]

        if len(eyes) == 0:
            cv2.putText(photo, "Nothing was found", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.putText(photo, "Scale factor:" +  str(scale_factor), (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("photo", photo)
        cv2.imwrite(f"new-image-{i}.png", photo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
