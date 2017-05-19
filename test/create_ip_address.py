import random
import socket
import struct

with open("ip2iden",'w') as fw:
    for i in range(100):
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        iden = "s%02d"%(i)

        fw.write(ip+' '+iden+'\n')