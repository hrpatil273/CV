
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import pickle
import random
import os
import statistics 
from statistics import mode 
import pyrebase
from datetime import datetime
import pathlib
from time import sleep 

c_path=0
fname=""
# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

secretCode = ""
OverrideCode = "5315"
input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global input
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("Input reset!");
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C4) == 1):
        if input == secretCode:
            print("Code correct!")
            print(input)
            UploadToFbase(FaceRecStart())
            #exit()
			GPIO.output(14, GPIO.HIGH) # Turn on
			sleep(1) # Sleep for 1 second
			GPIO.output(14, GPIO.LOW)
        elif input== OverrideCode:
            print("Door Unlocked")
			#upload data to firebase
            #exit()
			GPIO.output(14, GPIO.HIGH) # Turn on
			sleep(1) # Sleep for 1 second
			GPIO.output(14, GPIO.LOW)
            # TODO: Unlock a door, turn a light on, etc.
        else:
            print("Incorrect code!")
            print(input)
            # TODO: Sound an alarm, send an email, etc.
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

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
	if file.exists() == False:
		l_path="unknown.png"
		#print ("File not exist")

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
	db.child("users").push(data)
	#print(Rec_name)
	#print(stref)
	#print(dt_string)
	#print(dti_string)
	db.child("users").child(now.strftime("%Y%m%d%H%M%S")).set(data)

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            if not checkSpecialKeys():
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
