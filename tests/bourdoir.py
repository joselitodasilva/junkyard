#!/usr/bin/env python

import socket, OSC, re, time, threading, math
import random

receive_address = '0.0.0.0', 7000

#setting up the board
def set():
	for laser in ports:
		GPIO.setup(laser, GPIO.OUT)

def on():
	for laser in ports:
		GPIO.output(laser, True)

def off():
	for laser in ports:
		GPIO.output(laser, False)

# Initialize the OSC server and the client.
s = OSC.OSCServer(receive_address)
s.addDefaultHandlers()

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

def fader_blue(add, tags, stuff, source):
	print("Add: {}, tags: {}, stuff: {}, source:{}.".format(add, tags, stuff, source))

s.addMsgHandler("/1/faderC", fader_blue)

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


