'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
        
    def _handle_PacketIn (self, event):
        packet = event.parsed
        if packet.type == ethernet.IP_TYPE:
            ipv4_packet = event.parsed.find("ipv4")
            print 'Src: %s, Dst: %s' % (ipv4_packet.srcip, ipv4_packet.dstip)
        
    def buildTable(filename):
        file_a = open('firewall-policies.csv', 'r').readlines()
        acl = []
        if file_a[0] == 'id,mac_0,mac_1\n':
            file_a.pop(0)
        for line in file_a:
            accessHash = {}
            line = line.split(',')
            side_a = line[1].strip()
            side_b = line[2].strip()
            accessHash['pair'] = (side_a, side_b)
            accessHash['access'] = True
            acl.append(accessHash)
        return acl




def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
