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
        self.services = {}


    def on_service_state_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
        #when a new mDNS service is added or updated get info on service
        if state_change is ServiceStateChange.Added or state_change is ServiceStateChange.Updated:
            info = zeroconf.get_service_info(service_type, name)
            
            #if service info exists and contains hrbeacon type property then process it
            if info:
                try:
                    type = info.properties[b'type']
                    if type == b'nordinbeacon':
                        #get ip/port of printer
                        addresses = ["%s" % (socket.inet_ntoa(addr)) for addr in info.addresses]
                        port = [(cast(int, info.port)) for addr in info.addresses]
                        #"%d" %
                        #get printer info
                        hostname = info.properties[b'name'].decode('UTF-8')
                        series = info.properties[b'series'].decode('UTF-8')
                        version = info.properties[b'version'].decode('UTF-8')
                        #add printers to dictionary
                        printerInfo = {"address": addresses[0], "stat": -1, "port": port[0], "series": series, "version": version}
                        #self.services[name] = hostname
                        self.services[name] = info
                        self.printers[hostname] = printerInfo
                        #print data
                        print("{}: {} at {}".format(state_change, hostname, addresses))
                        #print("    Hardware Series:{}".format(series))
                        #print("    Hardware Version:{}".format(version))
                        #self.checkPrinterStatus()
                except KeyError:
                    pass
                        
        elif state_change is ServiceStateChange.Removed:
            try:
                #hostname = self.services[name]
                hostname = self.services[name].properties[b'name'].decode('UTF-8')
                del self.printers[hostname]
                del self.services[name]
                print("Removed: {}".format(hostname))
            except KeyError:
                pass
                
    def removePrinters(self):
        self.zeroconf.unregister_all_services()
        self.printers.clear()
        self.services.clear()
            
    def checkPrinterStatus(self):
        for printer in list(self.printers):
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rpi_port = (self.printers[printer]["address"], 22)
            rpi_up = a_socket.connect_ex(rpi_port)
            a_socket.close()

            if rpi_up == 0:
               #print("Port is open")
               a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                self.zeroconf.close()
                sleep(5)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.removePrinters()
            self.zeroconf.close()
