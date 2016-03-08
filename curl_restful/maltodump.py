import requests
import json
import pycurl
import os
import shutil

def sample(work_path,sample_file):
	"""anlayze the malware sample
	@param sample_file: malware sample
	"""
	# upload malware to cuckoo
	REST_SERVER = "159.226.16.26"
	REST_PORT = "5455"
	REST_DOWNLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/pcap/get/"
	REST_UPLOAD_URL = "http://"+REST_SERVER+":"+REST_PORT+"/tasks/create/file"
	SAMPLE_FILE = sample_file

	with open(SAMPLE_FILE,"rb") as sample:
		multipart_file = {"file": ("temp_file_name",sample)}
		request = requests.post(REST_URL, files=multipart_file)

	# request.status_code = 200 ?
		
	json_decoder = json.JSONDecoder()
	task_id = json_decoder.decode(request.text)["task_id"]

	# task_id = None ?

	# transfer result to log
	if 'samples' not in os.listdir(work_path):
		os.makedirs('samples/'+task_id)
	shutil.copy(filename,work_path+'/samples/'+task_id)
	os.chdir('samples/'+task_id)
	
	# get network dump of the sample from cuckoo
	dump_url = REST_DOWNLOAD_URL+task_id
	with open('out.pcap','wb') as f:
		c = pycurl.Curl()
		c.setopt(c.RUL,dump_url)
		c.setopt(c.WRITEDATA,f)
		c.perform()
		c.close()
	
	os.system('bro -r out.pcap local')

	
def main(filename):
	""" get malware network behavior from cuckoo and transfer pcap to log
	@param filename: filename of malware sample or .pcap file
	"""

	WORK_PATH = os.getcwd()
	if '.pcap' in filename:
		if 'pcapfiles' not in os.listdir(WORK_PATH):
			os.mkdir('pcapfiles')
		subdir = str(len(os.listdir(WORK_PATH+'/pcapfiles')))
		shutil.copy(filename,WORK_PATH+'/pcapfiles'+subdir)
		os.chdir('pcapfiles/'+subdir)
		os.system('bro -r '+filename+' local')
	else:
		smaple(WORK_PATH,filename)
	
if __name__ == "__main__":
	main(sys.args[1:])