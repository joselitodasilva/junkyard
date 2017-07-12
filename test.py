#File utilised in Junkyard Circus Crane Lights
#running on raspberry pi 3 with Motor Zero controller lighting up LED Strip
#powered by 8 AA batteries and controller via OSC from Phone (also wifi ssd)

"""OSC Test Script
Written by Aaron Chamberlain Dec. 2013
The purpose of this script is to make a very simple communication structure to the popular 
application touchOSC. This is achieved through the pyOSC library. However, since the pyOSC 
documentation is scarce and only one large example is included, I am going to strip down 
the basic structures of that file to implement a very simple bi-directional communication.
"""

#!/usr/bin/env python

import socket, OSC, re, time, threading, math
from time import sleep
#import RPi.GPIO as GPIO
#from blinkt import set_pixel, show, set_brightness
import random

receive_address = '0.0.0.0', 7000 #Mac Adress, Outgoing Port
send_address = '192.168.43.1', 9000 #iPhone Adress, Incoming Port

led1a = 27
led1b = 24
ledenable = 5

GPIO.setmode(GPIO.BCM)

GPIO.setup(led1a, GPIO.OUT)
GPIO.setup(led1b, GPIO.OUT)
GPIO.setup(ledenable, GPIO.OUT)

GPIO.output(led1a, GPIO.HIGH)
GPIO.output(led1b, GPIO.LOW)
GPIO.output(ledenable, GPIO.HIGH)

class PiException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

##########################
#	OSC
##########################

# Initialize the OSC server and the client.
s = OSC.OSCServer(receive_address)
c = OSC.OSCClient()
#c.connect(send_address)
s.addDefaultHandlers()
me = {
	0:{'r':0,'g':0,'b':0}, 
	1:{'r':0,'g':0,'b':0},
	2:{'r':0,'g':0,'b':0},
	3:{'r':0,'g':0,'b':0},
	4:{'r':0,'g':0,'b':0},
	5:{'r':0,'g':0,'b':0},
	6:{'r':0,'g':0,'b':0},
	7:{'r':0,'g':0,'b':0}
}

# define a message-handler function for the server to call.
def test_handler(addr, tags, stuff, source):
	print "---"
	print "received new osc msg from %s" % OSC.getUrlStr(source)
	print "with addr : %s" % addr
	print "typetags %s" % tags
	print "data %s" % stuff
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "return message %s" % msg
	print "---"

def moveStop_handler(add, tags, stuff, source):
	addMove(0,0)

def moveJoystick_handler(add, tags, stuff, source):
	print "message received:"
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "X Value is: " 
	print stuff[0] 
	print "Y Value is: " 
	print stuff[1]  #stuff is a 'list' variable

def fader_func(add, tags, stuff, source):
	print add
	print tags
	print stuff
	print source
	if stuff[0] > 0.5:
		print "GOOOOOOOO"

def fader_red(add, tags, stuff, source):
	global me
	r = stuff[0]*255
	for led in range(0,7):
		set_pixel(led, r, me[led]['g'], me[led]['b'])
		me[led]['r'] = r
	show()

def fader_green(add, tags, stuff, source):
        global me
        g = stuff[0]*255
        for led in range(0,7):
                set_pixel(led, me[led]['r'], g, me[led]['b'])
                me[led]['g'] = g 
        show()

def fader_blue(add, tags, stuff, source):
        global me
        b = stuff[0]*255
        for led in range(0,7):
                set_pixel(led, me[led]['r'], me[led]['g'], b)
                me[led]['b'] = b
        show()


#def fader_green(add, tags, stuff, source):
#        for led in range(0,7):
#                set_pixel(led,0,255,0,stuff[0])
#        show()
#
#def fader_blue(add, tags, stuff, source):
#        for led in range(0,7):
#                set_pixel(led,0,0,255,stuff[0])
#        show()

def jamming(addr, tags, stuff, source):
	for led in range(0,7):
		set_pixel(led, random.randint(1,256), random.randint(1,256), random.randint(1,256), random.random())
	show()
	#	set_pixel(led, me[led]['r'], me[led]['g'], me[led]['b'])
	#	show()

def set_bright(addr, tags, stuff, source):
	set_brightness(stuff[0])
	show()
	
def flick(addr, tags, stuff, source):
    for f in range(0,4):
        randommil = random.randint(80,120) / 1000.0
        #print randommil
        GPIO.output(ledenable, GPIO.HIGH)
        sleep(randommil)
        GPIO.output(ledenable, GPIO.LOW)
        sleep(randommil)
        GPIO.output(ledenable, GPIO.HIGH)


def ledon(addr, tags, stuff, source):
    GPIO.output(ledenable, GPIO.HIGH)

def ledoff(addr, tags, stuff, source):
    GPIO.output(ledenable, GPIO.LOW)
    

# adding my functions
s.addMsgHandler("/1/faderA", fader_green)
s.addMsgHandler("/1/faderB", fader_red)
s.addMsgHandler("/1/faderC", fader_blue)
s.addMsgHandler("/encoderM", jamming)
s.addMsgHandler("/1/faderD", set_bright)
s.addMsgHandler("/1/push5", flick)
s.addMsgHandler("/1/push7", ledon)
s.addMsgHandler("/1/push8", ledoff)



s.addMsgHandler("/composition/disconnectall", test_handler)
s.addMsgHandler("/activelayer/video/rotatez/playmode", test_handler)
#s.addMsgHanlder("


#s.addMsgHandler("/1/tagleA_1", test_handler)
s.addMsgHandler("/basic/stop", moveStop_handler)
s.addMsgHandler("/basic/joystick", moveJoystick_handler)


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
#s.serve_forever()
st = threading.Thread( target = s.serve_forever )
st.start()

# Loop while threads are running.
try :
	while 1 :
		time.sleep(10)
 
except KeyboardInterrupt :
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()

	print "Done"
