#! /usr/bin/env python

# Echo client program
import socket
import time
import datetime
import thread
import signal
import json
HOST='homeserver'
SERVER = 'hyperion'    # The remote host
PORT = 50007              # The same port as used by the server

OPEN=False
def createSocket():
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init():
	createSocket()
	time.sleep(1)
	s.connect((SERVER,PORT))

def beat():
	time.sleep(1)
	ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	data=json.dumps({"host":HOST,"time":ts,"timestamp":time.time()})
	s.send(data)

def beating():
	while 1:
		try:
			if not OPEN:
				init()	
			OPEN=True
			beat()	
			print 'beating'
		except KeyboardInterrupt:
			print 'Beating has been interminated'
			s.close()
			exit()
		except:
			OPEN=False
			print 'Connection Lost'

createSocket()
beating()
s.close()	

#data = s.recv(1024)
#print 'Received ', repr(data)

