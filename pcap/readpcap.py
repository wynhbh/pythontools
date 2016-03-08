#!/usr/bin/env python  
import sys

script,f = sys.argv
 
try:  
    import scapy.all as scapy  
except ImportError:  
    import scapy  
  
packets = scapy.rdpcap(f)

print 'packets:',len(packets)

for p in packets:
    print '=' * 70
    print dir(p)
