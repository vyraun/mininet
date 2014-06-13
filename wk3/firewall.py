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
        self.fwl = self.buildTable(policyFile)
        

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
        for rule in self.fwl:
            match = of.ofp_match()
            match.dl_src = EthAddr(rule['pair'][0])
            match.dl_dst = EthAddr(rule['pair'][1])
            msg = of.ofp_flow_mod()
            msg.match = match
            msg.priority = rule['priority']
            event.connection.send(msg)
            
            
        '''
        match = of.ofp_match()
        match.dl_src = EthAddr('00:00:00:00:00:01')
        match.dl_dst = EthAddr('00:00:00:00:00:02')
        msg = of.ofp_flow_mod()
        msg.match = match
        event.connection.send(msg)
        
        match = of.ofp_match()
        match.dl_src = EthAddr('00:00:00:00:00:02')
        match.dl_dst = EthAddr('00:00:00:00:00:01')
        msg = of.ofp_flow_mod()
        msg.match = match
        event.connection.send(msg)
        '''
        
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
        
    def _handle_PacketIn (self, event):
        packet = event.parsed
    	if packet.type == packet.IP_TYPE:
    		ipv4_packet = packet.find("ipv4")
            	log.debug('Src: %s(%s), Dst: %s(%s)' % (ipv4_packet.srcip, packet.src, ipv4_packet.dstip, packet.dst))
            
    def buildTable(self, filename):
        file_a = open('firewall-policies.csv', 'r').readlines()
        acl = []
        if file_a[0] == 'id,mac_0,mac_1\n':
            file_a.pop(0)
        for line in file_a:
            accessHash = {}
            line = line.split(',')
            priority = int(line[0])
            side_a = line[1].strip()
            side_b = line[2].strip()
            accessHash['pair'] = (side_a, side_b)
            accessHash['access'] = False
            accessHash['priority'] = priority
            acl.append(accessHash)
        return acl




def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
