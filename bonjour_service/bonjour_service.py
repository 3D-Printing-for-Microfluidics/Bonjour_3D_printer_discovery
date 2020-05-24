#!/usr/bin/env python3

""" Example of announcing a service (in this case, a HTTP server) """

import argparse
import socket
from time import sleep
from zeroconf import IPVersion, ServiceInfo, Zeroconf, NonUniqueNameException
import fcntl
import struct

HARDWARE_SERIES = "HR"
HARDWARE_VERSION = "3.3"

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', b'wlan0'))[20:24])
        except OSError:
            sleep(1)
                                
class IPBroadcaster():
    def __init__(self):
        print("Starting service")
        self.ip_version = IPVersion.V4Only
        self.service = None
        self.hostname = ""
        self.ip_address = ""
        self.zeroconf = None
        
    def __del__(self):
        print("Stopping service")
        self.zeroconf.close()
        
    def createService(self):
        self.hostname = socket.gethostname()
        self.ip_address = get_ip_address()

        desc = {'type': 'nordinbeacon', 'name': self.hostname, 'series': HARDWARE_SERIES, 'version': HARDWARE_VERSION}

        return ServiceInfo(
            "_http._tcp.local.",
            "{}._http._tcp.local.".format(self.hostname),
            addresses=[socket.inet_aton(self.ip_address)],
            port=5000,
            properties=desc,
            server="{}.local.".format(self.hostname),
        )
    
    def start(self):
        try:
            self.zeroconf.unregister_service(self.service)
            self.zeroconf.close()
        except AttributeError:
            pass
        self.service = self.createService()
        print("Registering mDNS")
        self.zeroconf = Zeroconf(ip_version=self.ip_version)
        try:
            self.zeroconf.register_service(self.service)
        except NonUniqueNameException:
            print("Nonunique-error")

#start broadcast
b = IPBroadcaster()
b.start()
while True:
    sleep(60)
    b.start()
