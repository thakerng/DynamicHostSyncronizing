DynamicHostSyncronizing
=======================

  This project is developed in Python and used for updating /etc/hosts automatically when your home-server's public IP address has been changed because of ISP. The project requires at least one static IP server outside to record fluctuated ip address from home-server.
  
Requirement
=======================
- Static IP server (OS: any Linux Distro )
- Home-Server installed python

Installation
=======================

1. Copy odind folder to static IP server in any path and make odind folder in /var/log ( For recording Log file ) 
2. You can config any parameters such as port or ip address in odin.py  
3. Append followed comment into /etc/host to make zone of dynamic hostname
``` 
      # dynamic.start:
      
      # :dynamic.end 
```
4. Open odind folder and run server with this command 
      ```run python odind.py start ```
  (This process will run in daemon mode)
5. Copy thor folder into home-server 
6. You can config any parameters such as port or hostname (default is homeserver) in thor.py 
7. Open thor folder and run client with this command 
      ```python thord.py start ```
   (This process will also run in daemon mode)
8. Test by ping to <hostname> in Static IP Server
