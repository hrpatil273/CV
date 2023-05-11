import time
import numpy as np
import cv2
import pickle
import random
import os
#from playsound import playsound
import statistics 
from statistics import mode 
import time
import pyrebase
from datetime import datetime
import pathlib

c_path=0
fname=""
Rec_name = ""


def FaceRecStart():
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

	cap = cv2.VideoCapture(0)
	start = time.time()

	c_path = random.randint(0, 10000)
	img="unknown.png"
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
				if conf>=81 and conf <= 90:
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

				img_item = "img/"+str(c_path)+".png"
				#print(img_item)	
				cv2.imwrite(img_item, frame)
				color = (255, 0, 0) #BGR 0-255 
				stroke = 2
				end_cord_x = x + w
				end_cord_y = y + h
				cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
			cv2.imshow('frame',frame)
			cv2.imwrite(img, frame)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		else:
			break
	cap.release()
	cv2.destroyAllWindows()
	fname="000"
	if reclable: 
		print("Recognised as :",mode(reclable))
		fname=mode(reclable)
		print("Face Authenticated, Welcome to the Home") 
		#playsound('welcome.mp3')
	else:
		print("Recognised as : Unknown")
		fname="Unknown"
		print("Unable to Recognize your face, Admin is informed about your presence")
		#playsound('unknown.mp3')
	return fname

def UploadToFbase(Rec_name):
	now = datetime.now()
	c_path = now.strftime("%Y%m%d%H%M%S")
	# print("date", dt_string)
	# print("time", dti_string)
	print("time", now)
	print("Uploading data to firebase")
	config={
		"apiKey": "AIzaSyCVfgS54LFJTjUKm53vStgODJjMDJ-EPTE",
		"authDomain": "mp-flutter-app.firebaseapp.com",
		"databaseURL": "https://mp-flutter-app-default-rtdb.firebaseio.com",
		"projectId": "mp-flutter-app",
		"storageBucket": "mp-flutter-app.appspot.com",
		"messagingSenderId": "1047382529102",
		"appId": "1:1047382529102:web:803614db0e423028bb5f1f",
		"measurementId": "G-0YZYZLSJ0S"
	};
	
	cl_path="img/"+str(c_path)+".png"
	l_path="img/"+str(c_path)+".png"
	file = pathlib.Path(l_path)
	print 
	if file.exists ():
		print ("File exist")
	else:
		l_path="unknown.png"
		print ("File not exist")

	firebase = pyrebase.initialize_app(config)
	storage = firebase.storage()
	storage.child(cl_path).put(l_path)
	stref = storage.child(cl_path).get_url(None)
	dt_string = now.strftime("%B %d, %Y")
	# dti_string = now.strftime("%A, %H:%M:%S")
	dti_string = now.strftime("%H:%M")
	db = firebase.database()
	data = {"name": Rec_name,
			"image" : stref,
			"date": dt_string,
			"time": dti_string}
	#db.child("users").push(data)
	print(Rec_name)
	print(stref)
	print(dt_string)
	print(dti_string)
	db.child("users").child(now.strftime("%Y%m%d%H%M%S")).set(data)



UploadToFbase(FaceRecStart())