import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import os
import copy

__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))  # directory from which this script is ran


class FaceTracker(object):

	def __init__(self,camera_index):
		#self.conf = conf
		self.cap = cv2.VideoCapture(int(camera_index))
		self.face_cascade = cv2.CascadeClassifier(os.path.join(__location__,'resources/haarcascade_frontalface_default.xml'))
		self.no_movement_command = ['n0','n0']

	def getFaceCommand(self):
		# what to return
		command = None
		# get image
		ret = False
		ret = self.cap.grab()
		if ret:
			ret,frame = self.cap.retrieve()
			
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			largestFace = self.findLargestFace(faces)

			if largestFace != None:
				x,y,w,h = largestFace
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
				# height and width
				frameh,framew = frame.shape[:2]
				# figure out buffer area
				h_buffer = frameh/12;
				w_buffer = framew/12;
				# get center of face
				center_x,center_y = ((x+x+w)/2,(y+y+h)/2)
				#print "Buffer W: %s\nBuffer H: %s" % (w_buffer,h_buffer)
				#print "Center X: %s\nCenter Y: %s" % (center_x,center_y)
				#print "Frame W: %s\nFrame H: %s" % (framew,frameh)
				# find out where camera must move to focus better
				command = []
				if (center_x < framew/2-w_buffer):
					command.append('p'+str(abs(framew/2-center_x)/w_buffer))
				elif (center_x > framew/2+w_buffer):
					command.append('m'+str(abs(framew/2-center_x)/w_buffer))
				else:
					command.append('n0')

				if (center_y < frameh/2-h_buffer):
					command.append('p'+str(abs(frameh/2-center_y)/h_buffer))
				elif (center_y > frameh/2+h_buffer):
					command.append('m'+str(abs(frameh/2-center_y)/h_buffer))
				else:
					command.append('n0')

			else:
				command = ['n0','n0']

			cv2.imshow('frame',frame)
		else:
			#print 'frame could not be grabbed'
			pass
		# use cv2 wait in order to display window
		key = cv2.waitKey(1) & 0xFF
		
		return command

	def findLargestFace(self,faces):
		largestArea = 0
		largestFace = None
		for (x,y,w,h) in faces:
			area = w*h
			if (area > largestArea):
				largestArea = area
				largestFace = (x,y,w,h)
		return largestFace

	def getNoMovementCommand(self):
		return copy.copy(self.no_movement_command)

	def stop(self):
		# When everything is done, release the capture
		self.cap.release()
		cv2.destroyAllWindows()
