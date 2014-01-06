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
TIMESLOT=3   #Success timeslot
TIMEDELAY=3  #Time delay after
#OPEN=False
class Thor:
	def __init__(self,server,port,host):
		self.isopen=False
		self.server=server
		self.port=port
		self.host=host

	def createSocket(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def open(self):
		self.createSocket()
		time.sleep(TIMEDELAY)
		self.s.connect((self.server,self.port))

	def beat(self):
		time.sleep(TIMESLOT)
		ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		data=json.dumps({"host":self.host,"time":ts,"timestamp":time.time()})
		self.s.send(data)

	def beating(self):
		while 1:
			try:
				if not self.isopen:
					self.open()	
				self.isopen=True
				self.beat()	
				print 'beating'
			except KeyboardInterrupt:
				print 'Beating has been interminated'
				self.s.close()
				exit()
			except:
				self.isopen=False
				print 'Connection Lost'

	def run(self):
		self.createSocket()
		self.beating()
		self.s.close()	
		
#data = s.recv(1024)
#print 'Received ', repr(data)

