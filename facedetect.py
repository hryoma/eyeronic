import cv2
from PIL import Image, ImageOps
import os

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")


def find_eyes(filepath):
    file_name = filepath.split('/')[1]
    # todo: i think there's error here, when the directory is already made
    os.mkdir('eyes/' + file_name + '/')

    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eye_count = 0

    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            img_eye = Image.open(filepath)
            img_eye = img_eye.crop((ex + x, ey + y, ex + ew + x, ey + eh + y))
            img_eye = ImageOps.grayscale(img_eye)
            img_eye = img_eye.resize((80, 80))
            img_eye.save('eyes/' + file_name + '/eye-' + str(eye_count) + ".jpg")
            eye_count += 1

