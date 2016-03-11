#!/usr/bin/env python
# This file is to get network logs of malware sample or .pcap traffic file
#

import requests
import json
import pycurl
import os
import sys
import shutil
import logging
import logging.handlers
import md5
import time


LOG_FILE = "maltodump.log"  # record the analyzing process
handler = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('maltodump')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def sample(file_path,sample_file):
	"""anlayze the malware sample
	@param sample_file: malware sample
	"""
	# upload malware to cuckoo
	REST_SERVER = "10.10.4.229"
	REST_PORT = "5455"
	REST_DOWNLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/pcap/get/"
	REST_UPLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/tasks/create/file"
	REST_TASK_VIEW = "http://"+REST_SERVER+":"+REST_PORT+"/tasks/view/"
	SAMPLE_FILE = sample_file
	
	with open(SAMPLE_FILE,"rb") as s:
		multipart_file = {"file": ("temp_file_name",s)}
		request = requests.post(REST_UPLOAD_URL, files=multipart_file)

	# request.status_code = 200 ?

	# task_id from cuckoo
	task_id = request.json()["task_id"]
	
	# return task_id < 0, meaning sth is wrong, like an analyzed sample.
	if task_id < 0:
		logger.error("task_id is "+str(task_id)+", which is out of expectation.")
		return
	
	# wait util cuckoo finished running
	taks_view_url = REST_TASK_VIEW+str(task_id)
	r = requests.get(taks_view_url)
	while(r.json()["task"]["status"] != "completed"):
		time.sleep(5)
		r = requests.get(taks_view_url)
	
	# get network dump of the sample from cuckoo
	os.chdir(file_path+'/logs')
	dump_url = REST_DOWNLOAD_URL+str(task_id)
	with open('out.pcap','wb') as f:
		c = pycurl.Curl()
		c.setopt(c.URL,dump_url)
		c.setopt(c.WRITEDATA,f)
		c.perform()
		c.close()
	
	os.system('bro -r out.pcap local')
	logger.info(sample_file+' has been processed successfully, resulting logs are in '+ file_path+'/logs')


def main(filename):
	""" get malware network behavior from cuckoo and transfer pcap to log
	@param filename: filename of malware sample or .pcap file
	"""
	
	WORK_PATH = os.getcwd()
	logger.info('Working path is '+WORK_PATH+', file '+filename+' is going to be processed.')
	
	if 'samples' not in os.listdir(WORK_PATH):
		os.mkdir('samples')

	with open(filename) as f:
		file_data = f.read()
		file_md5 = md5.new(file_data).hexdigest()
	
	## check if this file has been analyzed. search md5 from databases;
	# todo
	#
	
	
	ctime = str(int(time.time()))
	file_path = ctime+'_'+file_md5

	os.makedirs('samples/'+file_path+'/files')		# path ./files to keep the sample
	os.makedirs('samples/'+file_path+'/logs')			# path ./logs to keep the results

	shutil.copy(WORK_PATH+'/'+filename,WORK_PATH+'/samples/'+file_path+'/files')
	logger.info(filename+' has been copied to '+ WORK_PATH+'/samples/'+file_path+'/files')

	if '.pcap' in filename:
		logger.info(filename+' is a pcap file.')
		
		shutil.copy(WORK_PATH+'/'+filename,WORK_PATH+'/samples/'+file_path+'/logs')
		os.chdir('samples/'+file_path+'/logs')
		os.system('bro -r '+filename+' local')
		logger.info(filename+' has been processed successfully, resulting logs in '+ WORK_PATH+'/samples/'+file_path+'/logs')
	else:
		logger.info(filename+' is a malware sample.')

		sample(WORK_PATH+'/samples/'+file_path,filename)
	
if __name__ == "__main__":
	main(sys.argv[1])