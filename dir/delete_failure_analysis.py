import os
from os.path import join, getsize

begindir = "/home/cuckoo/cuckoo-master/storage/analyses"
for root, dirs, files in os.walk(begindir):
	if 'memory.dmp' in files:
		com = 'rm '+root+'/memory.dmp'
		print com
		os.system(com)
	#for name in dirs:
	#	print name

