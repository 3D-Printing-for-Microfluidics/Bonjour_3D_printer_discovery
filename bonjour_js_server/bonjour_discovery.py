#zeroconf
import argparse
import socket
from time import sleep
import time
from typing import cast
from zeroconf import (
    IPVersion,
    DNSHinfo,
    DNSText,
    ServiceBrowser,
    ServiceInfo,
    ServiceStateChange,
    Zeroconf,
    ZeroconfServiceTypes,
)

class BonjourDiscovery():

    def __init__(self):
        self.zeroconf = None
        self.printers = {}
        self.devices = {}
        self.services = {}
        self.timestamps = {}


    def on_service_state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        #when a new mDNS service is added or updated get info on service
        if state_change is ServiceStateChange.Added or state_change is ServiceStateChange.Updated:
            info = zeroconf.get_service_info(service_type, name)
            
            #if service info exists and contains hrbeacon type property then process it
            if info:
                try:
                    type = info.properties[b'type']
                    if 'nordin' in type.decode('UTF-8'):
                        #get ip/port of printer
                        addresses = ["%s" % (socket.inet_ntoa(addr)) for addr in info.addresses]
                        port = [(cast(int, info.port)) for addr in info.addresses]
                        #get printer info
                        hostname = info.properties[b'name'].decode('UTF-8')
                        series = info.properties[b'series'].decode('UTF-8')
                        version = info.properties[b'version'].decode('UTF-8')
                        #add printers to dictionary
                        printerInfo = {"address": addresses[0], "stat": -1, "port": port[0], "series": series, "version": version}

                        self.services[name] = info
                        self.timestamps[name] = time.time()
                        if type == b'nordin_printer':
                            self.printers[hostname] = printerInfo
                            print("PRINTER: {}: {} at {}".format(state_change, hostname, addresses))
                        elif type == b'nordin_device':
                            self.devices[hostname] = printerInfo
                            print("DEVICE: {}: {} at {}".format(state_change, hostname, addresses))
                        else:
                            print("NOT ADDED: {}: {} at {}".format(state_change, hostname, addresses))
                        #print data
                        #print("{}: {} at {}".format(state_change, hostname, addresses))
                        #print("    Hardware Series:{}".format(series))
                        #print("    Hardware Version:{}".format(version))
                except KeyError:
                    pass
                        
        elif state_change is ServiceStateChange.Removed:
            try:
                #hostname = self.services[name]
                hostname = self.services[name].properties[b'name'].decode('UTF-8')
                #try removing as printer
                try:
                    del self.printers[hostname]
                except KeyError:
                    pass
                #else try removing as device
                try:
                    del self.devices[hostname]
                except KeyError:
                    pass
                del self.services[name]
                del self.timestamps[name]
                print("Removed: {}".format(hostname))
            except KeyError:
                pass
                
    def removePrinters(self):
        self.zeroconf.unregister_all_services()
        self.printers.clear()
        self.devices.clear()
        self.services.clear()
        self.timestamps.clear()
        
    def removePrinter(self, name):
        hostname = self.services[name].properties[b'name'].decode('UTF-8')
        #try removing as printer
        try:
            del self.printers[hostname]
        except KeyError:
            pass
        #else try removing as device
        try:
            del self.devices[hostname]
        except KeyError:
            pass
        del self.services[name]
        del self.timestamps[name]
        print("Removed: {}".format(hostname))
            
    def checkPrinterStatus(self):
        for printer in list(self.printers):
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(2)
            rpi_port = (self.printers[printer]["address"], 22)
            rpi_up = a_socket.connect_ex(rpi_port)
            a_socket.close()

            if rpi_up == 0:
               #print("Port is open")
               a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               a_socket.settimeout(2)
               server_port = (self.printers[printer]["address"], self.printers[printer]["port"])
               server_up = a_socket.connect_ex(server_port)
               a_socket.close()

               if server_up == 0:
                  #print("Server is up")
                  self.printers[printer]["stat"] = 2
               else:
                  #print("Server is down")
                  self.printers[printer]["stat"] = 1
            else:
               #print("Port is not open")
               self.printers[printer]["stat"] = 0
               
    def checkDeviceStatus(self):
           for device in list(self.devices):
               a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               a_socket.settimeout(2)
               rpi_port = (self.devices[device]["address"], 22)
               rpi_up = a_socket.connect_ex(rpi_port)
               a_socket.close()

               if rpi_up == 0:
                  #print("Server is up")
                  self.devices[device]["stat"] = 2
               else:
                  #print("Port is not open")
                  self.devices[device]["stat"] = 0

            
    def loop(self):
        ip_version = IPVersion.V4Only
        try:
            while True:
                self.zeroconf = Zeroconf(ip_version=ip_version)

                print("\nBrowsing services\n")
                browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", handlers=[self.on_service_state_change])
                sleep(55)
                #for service in list(self.services):
                #    print("Reload {} {}".format(self.services[service].properties[b'name'].decode('UTF-8'), self.services[service].request(self.zeroconf, 5000)))
                #self.removePrinters()
                
                #delete devices that havn't updated in 10 minutes
                #(this does not account for cached mDNS entries, so it will take significantly longer then 10 minutes to remove a device)
                currentTime = time.time()
                for name in list(self.timestamps):
                    lastTime = self.timestamps[name]
                    if currentTime - lastTime > 600:
                        self.removePrinter(name)
                    
                self.zeroconf.close()
                sleep(5)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.removePrinters()
            self.zeroconf.close()
