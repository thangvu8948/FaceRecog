import cv2
import numpy as np
from PIL import Image
import pickle
import pyodbc

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainingData.yml")
id = 0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 0.5
fontcolor = (203, 23, 252)

#get data from sqlserver by ID
def getProfile(id):
    conn = pyodbc.connect(r'Driver={SQL Server};'
                          r'Server=DESKTOP-LVTN495\SQLEXPRESS;'
                          r'Database=FaceData;'
                          r'Trusted_Connection=yes;')
    cmd = "SELECT * FROM People where Id = " + str(id)
    cursor = conn.execute(cmd)
    profile=None
    for row in cursor:
        profile = row
    conn.close()
    return profile

while(True):
    #camera read
    ret, img = cam.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    cv2.imshow('Face', img)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h) , (255, 0 ,0), 2)
        id, conf = rec.predict(gray[y:y+h, x:x+w])
        profile = getProfile(id)
        #set text to window
        if (profile != None):
            cv2.putText(img, "Name: " + str(profile[1]), (x, y+h+30), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Age : " + str(profile[2]), (x, y+h+60), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Gender: " + str(profile[3]), (x, y+h+90), fontface, fontscale, fontcolor, 2)

        cv2.imshow('Face', img)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
