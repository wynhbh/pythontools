#!/usr/bin/env python
# This file is to get network logs of malware sample or .pcap traffic file
# coding: utf-8

import os
import sys
import string
import requests
import pycurl
import shutil
import md5
import time
import json
import logging
import logging.handlers
import ConfigParser
from database import Database, Model, Field, execute_raw_sql


LOG_FILE = "maltodump.log"  # record the analyzing process
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('maltodump')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Sample(Model):
    """ The malware sample model.
    """
    
    db_table = 'sample'
    
    id = Field()               # sample id
    file_MD5 = Field()         # sample file md5
    file_name = Field()        # sample file name
    submit_t  = Field()        # time of sample being submitted
    sample_path = Field()      # path of sample file stored
    log_path = Field()         # path of bro logs of sample
    mal_type = Field()         # sample type, if pcap type = 0 or not
    mal_tag = Field()          # sample tag, botnet or trojan ...
    mal_desc = Field()         # description of sample, like download URL


def process(file_path, file_name, log_path, REST_SERVER="10.10.4.229", REST_PORT="5455"):
    """anlayze the malware sample
    @param file_path: path to sample to be analyzed
    @param file_name: sample file name
    @param log_path: path of bro logs of sample
    @param REST_SERVER: server ip to run sample
    @param REST_PORT: port for restful api
    """

    # upload malware to cuckoo
    REST_DOWNLOAD_URL = 'http://%s:%s/pcap/get/' % (REST_SERVER, REST_PORT)
    REST_UPLOAD_URL = 'http://%s:%s/tasks/create/file' % (REST_SERVER, REST_PORT)
    REST_TASK_VIEW = 'http://%s:%s/tasks/view/' % (REST_SERVER, REST_PORT)
    SAMPLE_FILE = file_path +'/'+ file_name
    
    with open(SAMPLE_FILE,"rb") as s:
        multipart_file = {"file": ("temp_file_name",s)}
        request = requests.post(REST_UPLOAD_URL, files=multipart_file)

    # task_id from cuckoo
    task_id = request.json()["task_id"]
    
    # when task_id < 0, sth is wrong, like an analyzed sample.
    if task_id < 0:
        logger.error("task_id is %s, out of expectation" % (task_id))
        return
    
    # wait util cuckoo finished running
    taks_view_url = REST_TASK_VIEW+str(task_id)
    r = requests.get(taks_view_url)
    while(r.json()["task"]["status"] != "completed"):
        time.sleep(10)
        r = requests.get(taks_view_url)
    
    # get network dump of the sample from cuckoo
    os.chdir(log_path)
    dump_url = REST_DOWNLOAD_URL+str(task_id)
    with open('out.pcap','wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL,dump_url)
        c.setopt(c.WRITEDATA,f)
        c.perform()
        c.close()
    
    os.system('bro -r out.pcap local')
    logger.info('File %s processed, bro logs are in %s' % (file_name,log_path))


def run(WORK_PATH):
    """ run the analysis about the sample file.
    """
    
    logger.info('Working path is %s' % (WORK_PATH))
    submit_time = time.time()
    
    if 'samples' not in os.listdir(WORK_PATH):
        os.mkdir('samples')

    # get the information about the sample from config file
    sample_conf = ConfigParser.ConfigParser()
    sample_conf.read('sample.conf')
    
    sample_conf_path = sample_conf.get("sample","path")
    sample_conf_name = sample_conf.get("sample","name")
    sample_conf_type = sample_conf.getint("sample","type")
    sample_conf_tag = sample_conf.get("sample","tag")
    sample_conf_desc = sample_conf.get("sample","description")

    os.chdir(sample_conf_path)
    logger.info('Working path is %s' % (sample_conf_path))
    
    if sample_conf_name not in os.listdir(sample_conf_path):
        logger.error('There is no file %s in path %s' % (sample_conf_name, sample_conf_path))
        return

    with open(sample_conf_name) as f:
        file_data = f.read()
        file_md5 = md5.new(file_data).hexdigest()

    # anlayze the sample
    sample_Nm = Sample.where().count()
    if sample_Nm > 0 and Sample.where(file_MD5 = file_md5).count() > 0:
        logger.info('File %s has analyzed with md5: %s' % (sample_conf_name, file_md5))
        return
    else:
        sample = Sample()
        
        sample.id = sample_Nm
        sample.file_MD5 = file_md5
        sample.file_name = sample_conf_name
        sample.submit_t  = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(submit_time))
        sample.mal_type = sample_conf_type
        sample.mal_tag = sample_conf_tag
        sample.mal_desc = sample_conf_desc

        sub_path = str(int(submit_time))+'_'+file_md5
        sample.sample_path = '%s/samples/%s/files' % (WORK_PATH, sub_path)
        sample.log_path = '%s/samples/%s/logs' % (WORK_PATH, sub_path)

        sample.save()    # save sample information to database.
        
        os.makedirs(sample.sample_path)        # path ./files to keep the sample
        os.makedirs(sample.log_path)           # path ./logs to keep the results
    
        shutil.copy(sample_conf_path+'/'+sample_conf_name, sample.sample_path)
        logger.info('File %s has been copied to %s' % (sample_conf_name, sample.sample_path))

        if not sample.mal_type:
            shutil.copy(sample_conf_path+'/'+sample_conf_name, sample.log_path)
            os.chdir(sample.log_path)
            os.system('bro -r *.pcap local')
            logger.info('File %s processed, bro logs are in %s' % (sample_conf_name, sample.log_path))
        else:
            process(sample_conf_path, sample_conf_name, sample.log_path)
    
    return 


def main():
    """ get malware network behavior from cuckoo and transfer pcap to log
    """
    
    work_path = os.getcwd()
    
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'cuckoo',
        'password': 'analysis',
        'database': 'mal_traffic'
    }
    Database.connect(**db_config)

    run(work_path)
    
if __name__ == "__main__":
    main()