####################################################
# onvif camera network utils for discovery
#
# Author: fvilmos
# https://github.com/fvilmos
####################################################

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope

###################################################
# get all onvif devices IPs from the local network
###################################################
def get_onvif_devices():
    wsd = WSDiscovery()
    scope_test = Scope("onvif://www.onvif.org/Profile")
    
    wsd.start()
    services = wsd.searchServices(scopes=[scope_test])
    
    ips_ports = []
    for s in services:
        #get the urls, that looks like: http://<ip>/onvif/device_service
        ips_ports.append(str(s.getXAddrs()[0]))
    
    wsd.stop()

    return ips_ports

###############################################
# decode from urls the port and IP addresses
###############################################
def get_ips_ports(ips_ports:list=[]):
    
    ipl = []
    portl = []
    for ipp in ips_ports:
        ip = ipp.split('/')[2]
        if ':' in ip:
            # string has the port added too
            [ip,port]= ip.split(':')

        else:
            # just use the default port 80
            port = 80
        ipl.append(ip)
        portl.append(int(port))
    return ipl, portl