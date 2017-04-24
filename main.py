import time
from tracking.util import read_config, wait_till_done, TrackingException, UserInput
from comm.serialcomm import SerialComm
from tracking.trackinginterface import TrackingInterface

conf_dict = read_config("conf.txt")

# create interface for tracking faces
tracking = TrackingInterface(conf_dict)

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
		time.sleep(0.01)
	# otherwise, tell arduino how to center image
	else:
		wait_till_done(returnedCommandObj)

tracking.stop()
time.sleep(0.25)
