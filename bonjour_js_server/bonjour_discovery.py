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
                        addresses = ["%s:%d" % (socket.inet_ntoa(addr), cast(int, info.port)) for addr in info.addresses]
                        #get printer info
                        hostname = info.properties[b'name'].decode('UTF-8')
                        series = info.properties[b'series'].decode('UTF-8')
                        version = info.properties[b'version'].decode('UTF-8')
                        #add printers to dictionary
                        printerInfo = {"address": addresses[0], "series": series, "version": version}
                        self.services[name] = hostname
                        self.printers[hostname] = printerInfo
                        #print data
                        print("{}: {} at {}".format(state_change, hostname, addresses))
                        print("    Hardware Series:{}".format(series))
                        print("    Hardware Version:{}".format(version))
                except KeyError:
                    pass
                        
        elif state_change is ServiceStateChange.Removed:
            try:
                hostname = self.services[name]
                del self.printers[hostname]
                del self.services[name]
                print("Removed: {}".format(hostname))
            except KeyError:
                pass
                
    def removePrinters(self):
        for key in list(self.services):
            info = self.zeroconf.get_service_info("_http._tcp.local.", key)
            self.zeroconf.unregister_service(info)
            
    def loop(self):
        ip_version = IPVersion.V4Only

        try:
            while True:
                self.zeroconf = Zeroconf(ip_version=ip_version)

                print("\nBrowsing services\n")
                browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", handlers=[self.on_service_state_change])
                sleep(120)
                self.removePrinters()
                self.zeroconf.close()
                sleep(10)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.removePrinters()
            self.zeroconf.close()
