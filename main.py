import time
from tracking.util import read_config, wait_till_done, TrackingException
from comm.serialcomm import SerialComm
from tracking.trackinginterface import TrackingInterface

conf_dict = read_config("conf.txt")

# create ScrapInterface

tracking = TrackingInterface(conf_dict)
# for now, enter x and y coordinate to go to

# start user input thread
#userInput = UserInput()
#userInput.start()

while True:
	returnedCommandObj = tracking.trackFace()
	if returnedCommandObj == None:
		time.sleep(0.1)
	else:
		wait_till_done(returnedCommandObj)

tracking.stop()
time.sleep(0.25)
