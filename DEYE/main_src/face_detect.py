import numpy as np
import cv2
import time
import os
import random
import sys
import pickle
import statistics 
from statistics import mode 
import pyrebase
from datetime import datetime
now = datetime.now()
#print("date", dt_string)
#print("time", dti_string)

config={
	"apiKey": "AIzaSyBOUM83AbK23fok1ig_viMrnNdBPK71UCE",
    "authDomain": "upload-9d74d.firebaseapp.com",
    "databaseURL": "https://upload-9d74d.firebaseio.com",
    "projectId": "upload-9d74d",
    "storageBucket": "upload-9d74d.appspot.com",
    "messagingSenderId": "924809135420",
    "appId": "1:924809135420:web:4c85a7f4b108c2aa748a39",
    "measurementId": "G-64C6BR2X9E"
}

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

arr = []
reclable = []
flag=0


fps = 24
width = 864
height = 640
video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")

name = random.randint(0, 1000)
print(name)
if os.path.isdir(str(name)) is False:
    name = random.randint(0, 1000)
    name = "allRec\\"+str(name)

name = os.path.join(os.getcwd(), str(name))
print("ALl logs saved in dir:", name)
os.mkdir(name)


cap = cv2.VideoCapture(0)
ret = cap.set(3, 864)
ret = cap.set(4, 480)
cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


start = time.time()
video_file_count = 1
video_file = os.path.join(name, str(video_file_count) + ".avi")
print("Capture video saved location : {}".format(video_file))
#local path of video file
#l_path=format(video_file)

# Create a video write before entering the loop
video_writer = cv2.VideoWriter(
    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
)

while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    if ret == True:
        if time.time() - start > 8:
            break
        ret, frame = cap.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi_gray)
            if conf>=80 and conf <= 90:
                print(conf)
                arr.append(id_)
                print(flag)
                flag=flag+1
                print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                reclable.append(name)
                color = (255, 255, 255)
                stroke = 2
                #cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

            img_item = "7.png"
            cv2.imwrite(img_item, frame)
            l_path=img_item
            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        video_writer.write(frame)
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
if reclable: 
    print("Recognised as :",mode(reclable))
c_path = random.randint(0, 10000)	

cl_path="img/"+str(c_path)+".png"
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
storage.child(cl_path).put(l_path)
stref = storage.child(cl_path).get_url(None)
dt_string = now.strftime("%B %d, %Y")
dti_string = now.strftime("%A, %H:%M:%S")
db = firebase.database()
data = {"name": mode(reclable),
		"image" : stref,
		"date": dt_string,
		"time": dti_string}
db.child("users").push(data)