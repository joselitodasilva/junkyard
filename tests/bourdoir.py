#!/usr/bin/env python

import socket, OSC, re, time, threading, math
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#ports = [4, 5, 6, 19, 26, 21, 16, 23]
receive_address = '0.0.0.0', 7000

ports = {
    '/toggleA_1': 4,
    '/toggleA_2': 5,
    '/toggleB_1': 6,
    '/toggleB_2': 19,
    '/toggleC_1': 26,
    '/toggleC_2': 21,
    '/toggleD_1': 16,
    '/toggleD_2': 23 
    } 

#setting up the board
def set():
    for laser in ports.iteritems():
	print laser
        GPIO.setup(laser[1], GPIO.OUT)

def on():
    for laser in ports:
	GPIO.output(laser, True)

def off():
    for laser in ports:
        GPIO.output(laser, False)

# Initialize the OSC server 
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

def toggles(add, tags, stuff, source):
    True if stuff[0] == 1.0 else 'False'
    GPIO.output(ports[add], True if stuff[0] == 1.0 else False)

s.addMsgHandler("/1/faderC", fader_blue)
s.addMsgHandler("/multifaderM/4", fader_blue) #all on/off
for toggle in ports.keys():
    s.addMsgHandler(toggle, toggles)

#display handlers
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr

if __name__ == "__main__":
    set()
    # Start OSCServer
    print "\nStarting OSCServer. Use ctrl-C to quit."
    s.serve_forever()
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
