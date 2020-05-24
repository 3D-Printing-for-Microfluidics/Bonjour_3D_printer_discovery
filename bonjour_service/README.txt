
bonjour_service broadcasts this devices IP address, hostname, and hardware type as a mDNS device. The broadcast type is _http._tcp.local. with a type property of nordinbeacon.

To install:

1) Open terminal in this directory.
2) Run "sudo -s source bonjour_service_setup.sh"
3) Edit lines 12 and 13 in bonjour_service.py to show proper hardware
4) Reboot device