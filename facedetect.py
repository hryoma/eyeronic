import numpy as np
import cv2
from PIL import Image, ImageDraw
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
#save the image(i) in the same directory
img = cv2.imread("family.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
count = 0
for (x,y,w,h) in faces:
	img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = img[y:y+h, x:x+w]
	eyes = eye_cascade.detectMultiScale(roi_gray)
	for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            im = Image.open('family.jpg')
            print(ex,ey,ew+ex,ey+eh)
            im = im.crop((ex+x,ey+y,ex+ew+x, ey+eh+y))
            im = im.resize((80,80))
            im.save('croppedeyes'+str(count) +  ".jpg")
            count += 1
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
