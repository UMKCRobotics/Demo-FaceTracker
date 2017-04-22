import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import os
import serial

print "hello world"

def ard_init(ser):
	connected = False
	while not connected:
		serin = ser.read()
		connected = True

def findLargestFace(faces):
	largestArea = 0
	largestFace = None
	for (x,y,w,h) in faces:
		area = w*h
		if (area > largestArea):
			largestArea = area
			largestFace = (x,y,w,h)
	return largestFace

ser = serial.Serial('/dev/ttyACM0',115200)
#ser = serial.Serial('/dev/ttyACM0',57600)

ard_init(ser)
	
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '/'
if os.name == 'nt':
	location = location.replace('\\','/')

cap = cv2.VideoCapture(1)

face_cascade = cv2.CascadeClassifier(location + 'haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier(location + 'haarcascade_eye.xml')

faceBefore = False;
counter = 0
previous_command = None
command = None

while(True):
	# Capture frame-by-frame
	#ret, frame = cap.read()
	ret = False
	ret = cap.grab()
	if ret:
		ret,frame = cap.retrieve()
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		largestFace = findLargestFace(faces)

		if largestFace != None:
			faceBefore = True
			x,y,w,h = largestFace
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
			# height and width
			frameh,framew = frame.shape[:2]
			# figure out buffer area
			h_buffer = frameh/12;
			w_buffer = framew/12;
			# get center of face
			center_x,center_y = ((x+x+w)/2,(y+y+h)/2)
			print "Buffer W: %s\nBuffer H: %s" % (w_buffer,h_buffer)
			print "Center X: %s\nCenter Y: %s" % (center_x,center_y)
			print "Frame W: %s\nFrame H: %s" % (framew,frameh)
			# find out where camera must move to focus better
			command = ""
			if (center_x < framew/2-w_buffer):
				command += 'p'
				command += str(abs(framew/2-center_x)/w_buffer)
			elif (center_x > framew/2+w_buffer):
				command += 'm'
				command += str(abs(framew/2-center_x)/w_buffer)
			else:
				command += 'n0'

			if (center_y < frameh/2-h_buffer):
				command += 'p'
				command += str(abs(frameh/2-center_y)/h_buffer)
			elif (center_y > frameh/2+h_buffer):
				command += 'm'
				command += str(abs(frameh/2-center_y)/h_buffer)
			else:
				command += 'n0'

			command += '\n'

			if previous_command != 'n0n0\n' or previous_command != command:
				print "sending: " + command
				ser.write(command)
				received = ""
				while received.endswith('\n') != True:
					received += ser.read()
				print received

		else:
			if faceBefore:
				command = 'n0n0\n'
				ser.write(command)
				print 'sent that no movement required'
			faceBefore = False

		cv2.imshow('frame',frame)
		previous_command = command
	else:
		print 'frame could not be grabbed'
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()


