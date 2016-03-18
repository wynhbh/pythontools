#!/usr/bin/python

import pymongo
import random
import sys
import string

#script,i = sys.argv[0:]

client = pymongo.MongoClient("127.0.0.1",27017)
db = client.cuckoo
#rs = db.authenticate("pymongo","pwd123")
fw = open('positives','w')

#for item in db.analysis.find().limit(int(i)):
for item in db.analysis.find({"virustotal.positives":{"$gt":0}}):
	virustotal = item['virustotal']
	results = virustotal['scans']
	restr = []
	for si in results:
		if results[si]['detected']:
			restr.append(si+':'+results[si]['result'])
			#print subitem,subitem['detected'],subitem['result']
	fw.write(virustotal['md5']+','+str(virustotal['total'])+','+str(virustotal['positives'])+','+'|'.join(restr)+'\n')
fw.close()
