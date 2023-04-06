from flask import Flask, redirect, request, jsonify, render_template, url_for, session, Response

#camera

#from tkinter import Frame
import numpy as np
import cv2
#import math
import pyttsx3 

import HandTrackingModule as htm
import time
import autopy

from PIL import Image

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from imutils.video import VideoStream
import pyautogui

from keras.models import load_model
from time import sleep
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

engine = pyttsx3.init()
Wcam, Hcam = 640, 480
frameR = 100
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('database/training.xml')
cap = cv2.VideoCapture(0)
cap.set(3, Wcam)
cap.set(4, Hcam)
cap.set(cv2.CAP_PROP_BUFFERSIZE,3)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
smoothening = 5

plocX, plocY = 0, 0
clocX, clocY = 0, 0

face_classifier = cv2.CascadeClassifier(r'G:\CrevHim\Code\software\test\api-dashboard-monitor\flask camera\haarcascade_frontalface_default.xml')
classifier = load_model(r'G:\CrevHim\Code\software\test\api-dashboard-monitor\flask camera\model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']


def gen():
    #global id
    while True:
        global frame, pTime, plocX ,plocY, clocX,clocY
        success, frame = cap.read()
        img = detector.findHands(frame)
        # img =cv2.flip(img,1)
        lmList, bbox = detector.findPosition(img)
        
        #emotion detect
        
        labels = []
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]
                label=emotion_labels[prediction.argmax()]
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
           
        if len(lmList)!=0: 
            x0 , y0 = lmList[4][1:]
            x1 , y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = detector.fingersUp()
            if fingers[1] == 1 and fingers [2] == 0 and fingers[0] == 0:
                cv2.rectangle(img,(frameR,frameR), (Wcam-frameR, Hcam - frameR),
                          (255, 0, 255), 2)
                x3 = np.interp(x1, (frameR, Wcam-frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, Hcam-frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                #autopy.mouse.move(wScr - clocX, clocY)
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img,(x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX , clocY
            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 35.0:
                    cv2.circle(img,(lineInfo[4], lineInfo[5]),
                           15, (0, 255, 255), cv2.FILLED)
                    autopy.mouse.click()
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)), (20,50),cv2.FONT_HERSHEY_PLAIN,3,
        (255,0,0), 3)
        if not success:
            break
        else:
            img =cv2.flip(img,1)
            ret,buffer = cv2.imencode('.jpg',img)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #return id






flask_app = Flask(__name__)
@flask_app.route('/video')
def video(): 
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    flask_app.run(debug=True)