import sys
import oscserver

device = sys.platform

def osc(command):
	if command == "run":
		oscserver.start_osc()
	elif command == "stop":
		oscserver.stop_osc()
	else:
		print "Command not recognize. Running: {}".format(oscserver.running)

#class junkberry:
#	def defineType(self):
#		self.type = sys.platform
#
#	def osc(self, command):
#		if command == "run":
#			oscserver.start_osc()
#		elif command == "stop":
#			oscserver.stop_osc()
#		else:
#			print "Command not recognize. Running: {}".format(oscserver.running)