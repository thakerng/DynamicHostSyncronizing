#! /usr/bin/env python

# Echo server program
import socket
import time
import json
import subprocess
import os
from dynhost import MapHost
from dynhost import DynamicHost
class Odind:
	def __init__(self,host='',port=50007):
		self.host=host
		self.port=port
	def start(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.host, self.port))
		Edge=False
		while 1:
			try:
				print 'Listening on',self.port,' ...'
				s.listen(1)
				conn, addr = s.accept()
				print 'Connected by', addr
				ip,pot = addr
				with open("/var/log/odind/iphost", "a") as myfile:
		    			myfile.write(ip+"\n")
				while 1:
					data = conn.recv(1024)
					if not data: 
						break
					dataObject=json.loads(data)
					print 'host : ',dataObject['host'],' response : ',round((time.time()-dataObject['timestamp'])*1000,2),' ms DateTime : ',dataObject['time'];
					if not Edge:
						with open("/var/log/odind/iphost","a") as f:
							f.write(dataObject['host']+"\t"+ip+'\t'+dataObject['time']+'\n')	
						dynh=DynamicHost(dataObject['host'],ip)
					Edge=True
				conn.close()
				Edge=False
			except KeyboardInterrupt:
				print 'Server has been interminated'
				exit()
			except Exception,err:
				with open("/var/log/odind/iphost","a") as f:
					f.write(err)				
	def run(self):
		self.start()
