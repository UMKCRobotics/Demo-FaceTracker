import os, sys, time

# add relevant dir to path
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))  # directory from which this script is ran
main_dir = os.path.realpath(os.path.join(__location__,'../..'))
sys.path.insert(0, main_dir)

from util import TrackingException
from arduinointerface import ArduinoInterface
from facetracker import FaceTracker


class TrackingInterface(object):


	def __init__(self, conf):
		self.movement = ArduinoInterface(conf["ard_port"],conf["ard_baud"],conf["MAX_TRIES"])
		self.faceTracker = FaceTracker(conf["CAMERA_INDEX"])
		self.previous_command = None
		self.no_movement = self.faceTracker.getNoMovementCommand()

	def trackFace(self):
		new_command = self.faceTracker.getFaceCommand()
		if new_command is not None and not (new_command == self.no_movement and self.previous_command == self.no_movement):
			self.previous_command = new_command
			return self.movement.doCommand("m",new_command)
		else:
			return None
	
	def stop(self):
		self.movement.stop()
		self.faceTracker.stop()
