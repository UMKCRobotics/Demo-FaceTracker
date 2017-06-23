import time
from tracking.util import read_config, wait_till_done, TrackingException, UserInput
from comm.serialcomm import SerialComm
from tracking.trackinginterface import TrackingInterface
import cv2

conf_dict = read_config("conf.txt")
conf_dict["DEBUG"] = int(conf_dict["DEBUG"])

# open video camera
camera_obj = cv2.VideoCapture(int(conf_dict["CAMERA_INDEX"]))

# create interface for tracking faces
tracking = TrackingInterface(conf_dict,camera_obj)

# start user input thread
userInput = UserInput()
userInput.start()

while True:
	# check if there is a user message
	user_inp = userInput.returnMessage()
	if user_inp is not None and user_inp.lower().startswith("exit"):
		break
	# now do normal tracking behavior
	returnedCommandObj = tracking.trackFace()
	# if no face detected, sleep for a bit
	if returnedCommandObj == None:
		pass
	# otherwise, tell arduino how to center image
	else:
		if not conf_dict["DEBUG"]:
			wait_till_done(returnedCommandObj)
	time.sleep(0.02)

tracking.stop()
time.sleep(0.25)
