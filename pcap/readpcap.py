#!/usr/bin/env python  

try:  
    import scapy.all as scapy  
except ImportError:  
    import scapy  
  
packets = scapy.rdpcap('f:\\abc123.pcap')  
for p in packets:  
    print '=' * 70
	print p