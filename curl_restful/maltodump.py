import requests
import json
import pycurl
import os
import sys
import shutil
import logging
import logging.handlers
import time


LOG_FILE = "maltodump.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('maltodump')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def sample(work_path,sample_file):
	"""anlayze the malware sample
	@param sample_file: malware sample
	"""
	# upload malware to cuckoo
	REST_SERVER = "159.226.16.31"
	REST_PORT = "5455"
	REST_DOWNLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/pcap/get/"
	REST_UPLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/tasks/create/file"
	REST_TASK_VIEW = "http://"+REST_SERVER+":"+REST_PORT+"/tasks/view/"
	SAMPLE_FILE = sample_file
	

	with open(SAMPLE_FILE,"rb") as s:
		multipart_file = {"file": ("temp_file_name",s)}
		request = requests.post(REST_UPLOAD_URL, files=multipart_file)

	# request.status_code = 200 ?
		
	# json_decoder = json.JSONDecoder()
	# task_id = json_decoder.decode(request.text)["task_id"]
	task_id = request.json()["task_id"]
	
	
	# return task_id < 0, mean sth is wrong, like an analyzed sample.
	if task_id < 0:
		logger.error("task_id is "+str(task_id)+", maybe an analyzed sample")
		return
	
	task_id = str(task_id)

	# transfer result to log
	# if 'samples' not in os.listdir(work_path):
	
	os.makedirs('samples/'+task_id)
	shutil.copy(sample_file,work_path+'/samples/'+task_id)
	os.chdir('samples/'+task_id)
	
	# wait util cuckoo finished running
	taks_view_url = REST_TASK_VIEW+task_id
	r = requests.get(taks_view_url)
	while(r.json()["task"]["status"] != "completed"):
		time.sleep(5)
		r = requests.get(taks_view_url)
	
	# get network dump of the sample from cuckoo
	dump_url = REST_DOWNLOAD_URL+task_id
	with open('out.pcap','wb') as f:
		c = pycurl.Curl()
		c.setopt(c.URL,dump_url)
		c.setopt(c.WRITEDATA,f)
		c.perform()
		c.close()
	
	os.system('bro -r out.pcap local')
	logger.info(sample_file+' has been processed successfully, resulting logs are in '+ work_path+'/samples/'+task_id)

	
def main(filename):
	""" get malware network behavior from cuckoo and transfer pcap to log
	@param filename: filename of malware sample or .pcap file
	"""
	
	WORK_PATH = os.getcwd()
	logger.info('Working path is '+WORK_PATH+', file '+filename+' is going to be processed.')

	if '.pcap' in filename:
		logger.info(filename+' is a pcap file.')
		if 'pcapfiles' not in os.listdir(WORK_PATH):
			os.mkdir('pcapfiles')
		subdir = str(len(os.listdir(WORK_PATH+'/pcapfiles')))
		os.mkdir('pcapfiles/'+subdir)
		shutil.copy(WORK_PATH+'/'+filename,WORK_PATH+'/pcapfiles/'+subdir)
		os.chdir('pcapfiles/'+subdir)
		os.system('bro -r *.pcap local')
		logger.info(filename+' has been processed successfully, resulting logs are in '+ WORK_PATH+'/pcapfiles/'+subdir)
	else:
		logger.info(filename+' is a malware sample.')
		sample(WORK_PATH,filename)
	
if __name__ == "__main__":
	main(sys.argv[1])