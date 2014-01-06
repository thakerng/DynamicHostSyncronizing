#! /usr/bin/env python
class MapHost:
	def __init__(self,string):
		self.hosts=[]
		half=string.split('\t')
		self.ip=half[0]
		hosts=half[1].split(' ')
		for host in hosts:
			self.hosts.append(host)
	def getIP(self):
		return self.ip
	def getHosts(self):
		return self.hosts
	def setIP(self,ip):
		self.ip=ip
	def setHosts(self,hosts):
		self.hosts=hosts
	def addHost(self,host):
		if self.hosts.count(host)>0:
			return
		self.hosts.append(host)
	def addHosts(self,hosts):
		for host in hosts:
			addHost(host)
	def deleteHost(self,host):
		if self.hosts.count(host)>0:
			self.hosts.remove(host)
	def editHostName(self,host,newhost):
		if self.hosts.count(host)>0:
			i=self.hosts.index(host)
			self.hosts[i]=newhost
	def hasHost(self,host):
		if self.hosts.count(host)>0:
			return True
		return False
	def toString(self):
		string=self.ip+'\t'
		for host in self.hosts:
			string=string+host+' '
		return string
		
class DynamicHost:
	def __init__(self,host=False,ip=False,hosts='/etc/hosts'):
		self.hosts=hosts
		f=open(self.hosts,"r+")
		found=False
		state=0
		while 1:
			lines=f.readlines()
			if not lines:
				break
			for line in lines:
				if line.strip()==('# dynamic.start:') and state==0:
					state=1
				elif line.strip()==('# :dynamic.end') and state==1:
					found=True
					state=0
					break
			if not found:
				f.write('\n# dynamic.start:\n \n# :dynamic.end\n')
			break
		if host and ip:
			self.add(host,ip)

	def getHosts(self):
		print self.hosts
	def _get(self):
		mapHosts=[]
		f=open(self.hosts,"r")
		found=False
		state=0
		while 1:
			lines=f.readlines()
			if not lines:
				break
			for line in lines:
				if line.strip()==('# dynamic.start:') and state==0:
					list=""
					state=1
				elif line.strip()==('# :dynamic.end') and state==1:
					state=0
					break
				elif state==1:
					line=line.replace('\n','')
					if line.strip()=='':
						continue
					new=MapHost(line)
					mapHosts.append(new)
		return mapHosts
	def _updatefile(self,newData):
		wraptop=''
		wrapbottom=''
		state=0
		f=open(self.hosts,"r")
		while 1:
			lines=f.readlines()
			if not lines:
				break
			for line in lines:
				if line.strip()==('# dynamic.start:') and state==0:
					state=1
					wraptop=wraptop+'# dynamic.start:'
				elif line.strip()==('# :dynamic.end') and state==1:
					state=2
					wrapbottom=wrapbottom+'# :dynamic.end\n'
				elif state==0:
					wraptop=wraptop+line
				elif state==2:
					wrapbottom=wrapbottom+line
		f.close()
		f=open(self.hosts,"w")
		f.write(wraptop+'\n'+newData[:-1]+'\n'+wrapbottom)
		f.close()
	def clear(self):
		self._updatefile('')
	def update(self,maphosts):
		newData=''
		for host in maphosts:
			newData=newData+host.toString()+'\n'
		return self._updatefile(newData)
	def modify(self,host,ip):
		maphosts=self._get()
		ipfound=False
		hostfound=False
		for maphost in maphosts:
			if maphost.hasHost(host):
				maphost.setIP(ip)
				return maphosts
			elif maphost.getIP()==ip:
				maphost.addHost(host)
				return maphosts
		new=MapHost(ip+'\t'+host)
		maphosts.append(new)
		return maphosts
	def add(self,host,ip):
		newmaphosts=self.modify(host,ip)
		self.update(newmaphosts)		
		
