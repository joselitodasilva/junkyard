import OSC, threading, time

receive_address = "0.0.0.0", 7000

s = OSC.OSCServer(receive_address)
s.addDefaultHandlers()

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
        print addr

# Start OSCServer
def start_osc_server():
    print "\nStarting OSCServer."
    #s.serve_forever()
    st = threading.Thread( target = s.serve_forever )
    st.start()

    # just checking which handlers we have added
    print "Registered Callback-functions are :"
    for addr in s.getOSCAddressSpace():
        print addr

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
