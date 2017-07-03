import OSC, threading, time

host_address = "0.0.0.0", 7000
running = 0
s = None
st = None

def start_osc():
    global running, s, st
    
    if running == 1:
        print "\nOSCServer already running"
        return

    print "\nStarting OSCServer."
    s = OSC.OSCServer(host_address)
    s.addDefaultHandlers()
    #s.serve_forever()
    st = threading.Thread( target = s.serve_forever )
    st.start()
    running = 1
    # Display Handlers

    print "Registered Callback-functions are :"
    for addr in s.getOSCAddressSpace():
        print addr


def stop_osc():
    global running, s, st
    if running == 1:
        print "\nStopping OSCServer."
        s.close()
        st.join()
        print "\nOSC Server stopped"
