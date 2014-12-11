#! /usr/bin/env python
import sys, socket

try:
    result = socket.gethostbyaddr("192.168.1.101")
    print "Primary hostname:"
    print "  " + result[0]
    print result	
    # Display the list of available addresses that is also returned
    print "\nAddresses:"
    for item in result[2]:
        print "  " + item
except socket.herror, e:
    print "Couldn't look up name:", e

