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
    
    db_table = 'samples'
    
    id = Field()               # sample id
    file_MD5 = Field()         # sample file md5
    file_path = Field()        # path of sample file to be submitted
    file_name = Field()        # sample file name
    file_size = Field()        # file size of file
    submit_t  = Field()        # time of sample being submitted
    sample_path = Field()      # path of sample file to be stored
    log_path = Field()         # path of bro logs
    mal_type = Field()         # sample type, if pcap type = 0 or not
    mal_tag = Field()          # sample tag, botnet or trojan ...
    mal_desc = Field()         # description of sample, like download URL
    task_id = Field()          # task id when submitted to cuckoo
    cuckoo_tag = Field()       # malware type tagged by cuckoo


def init_db():
    """ init database connection for store processing information.
    """
  
    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read('db.conf')
    
    db_host = conf_parser.get("db","host")
    db_port = conf_parser.get("db","port")
    db_user = conf_parser.get("db","user")
    db_passwd = conf_parser.get("db","password")
    db_database = conf_parser.get("db","database")
    
    db_config = {
        'host': db_host,
        'port': db_port,
        'user': db_user,
        'password': db_passwd,
        'database': db_database
    }
    
    Database.connect(**db_config)

def upload_sample_cuckoo(SAMPLE_FILE, REST_SERVER, REST_PORT):
    """ upload the sample to cuckoo
    @param SAMPLE_FILE: the sample to be uploaded
    @param REST_SERVER: cuckoo server
    @param REST_PORT: cuckoo restful api port
    @return task_id: given by cuckoo, task_id will be a positive integer if upload seccessfully.  
    """

    REST_UPLOAD_URL = 'http://%s:%s/tasks/create/file' % (REST_SERVER, REST_PORT)       # upload malware to cuckoo

    with open(SAMPLE_FILE,"rb") as s:
        multipart_file = {"file": ("temp_file_name",s)}
        request = requests.post(REST_UPLOAD_URL, files=multipart_file)

    task_id = request.json()["task_id"]
    return task_id

def sample_pcap_process(task_id, REST_SERVER, REST_PORT):
    """ upload the sample to cuckoo
    @param task_id: task_id of the submiited sample in cuckoo
    @param REST_SERVER: cuckoo server
    @param REST_PORT: cuckoo restful api port  
    """

    REST_PCAP_URL = 'http://%s:%s/pcap/get/' % (REST_SERVER, REST_PORT)       # download pcap from cuckoo

    dump_url = REST_PCAP_URL+str(task_id)
    with open('out.pcap','wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL,dump_url)
        c.setopt(c.WRITEDATA,f)
        c.perform()
        c.close()
    
    os.system('bro -r out.pcap local')

    
def get_cuckoo_tag(task_id, REST_SERVER, REST_PORT):
    """ upload the sample to cuckoo
    @param task_id: task_id of the submiited sample in cuckoo
    @param REST_SERVER: cuckoo server
    @param REST_PORT: cuckoo restful api port
    @precondition: cuckoo must setup json report.
    """
    
    REST_REPORT_URL = 'http://%s:%s/tasks/report/' % (REST_SERVER, REST_PORT)
    
    report_url = REST_REPORT_URL+str(task_id)
    
    report = requests.get(report_url).json()

    av_res = {}

    # anti-virus products ordered as it's index.
    ants = [u'Avast', u'Microsoft', u'AVG', u'Avira', u'Symantec', u'McAfee', u'ESET-NOD32', u'Kaspersky', u'Comodo',
            u'BitDefender', u'Bkav', u'MicroWorld-eScan', u'nProtect', u'CAT-QuickHeal', u'Malwarebytes', u'VIPRE',
            u'AegisLab', u'TheHacker', u'K7GW', u'K7AntiVirus', u'Agnitum', u'F-Prot', u'TrendMicro-HouseCall',
            u'ClamAV', u'Alibaba', u'NANO-Antivirus', u'SUPERAntiSpyware', u'ByteHero', u'Rising', u'Ad-Aware',
            u'Sophos', u'F-Secure', u'DrWeb', u'Zillya', u'TrendMicro', u'McAfee-GW-Edition', u'Emsisoft', u'Cyren',
            u'Jiangmin', u'Antiy-AVL', u'Kingsoft', u'Arcabit', u'ViRobot', u'AhnLab-V3', u'GData', u'TotalDefense',
            u'ALYac', u'AVware', u'VBA32', u'Panda', u'Zoner', u'Tencent', u'Ikarus', u'Fortinet',
            u'Baidu-International', u'Qihoo-360']

    if "response_code" in report["virustotal"] and report["virustotal"]["response_code"] == 1:
        for av in report["virustotal"]["scans"]:
            if report["virustotal"]["scans"][av]["detected"]:
                av_res[av] = report["virustotal"]["scans"][av]["result"]
    else:
        logger.info("no virustotal responses: %s" % report)

    cuckoo_tags = []

    for i in ants:
        if i in av_res:
            cuckoo_tags.append("%s %s" % (i, av_res[i]))
        if len(cuckoo_tags) > 2:
            break

    return ';'.join(cuckoo_tags)

def process(sample, REST_SERVER, REST_PORT, timeout):
    """anlayze the malware sample through cuckoo
    @param sample: the sample to be processed
    @param REST_SERVER: cuckoo server
    @param REST_PORT: cuckoo restful api port
    """
    
    SAMPLE_FILE = sample.file_path +'/'+ sample.file_name
    REST_TASK_VIEW = 'http://%s:%s/tasks/view/' % (REST_SERVER, REST_PORT)      # get malware running status in cuckoo

    task_id = upload_sample_cuckoo(SAMPLE_FILE, REST_SERVER, REST_PORT)
    sample.task_id = task_id

    # when task_id < 0, sth is wrong, like an analyzed sample.
    if  task_id < 0:
        logger.error("task_id is %s, out of expectation" % (task_id))
        return
    
    # wait util cuckoo finished running
    taks_view_url = REST_TASK_VIEW+str(task_id)

    time_flag = 0
    r = requests.get(taks_view_url)
    while(r.json()["task"]["status"] != "completed"):
        time.sleep(10)
        time_flag += 10
        if time_flag > timeout:
            return      # no cuckoo pcap results
        r = requests.get(taks_view_url)

    os.chdir(sample.log_path)
    sample_pcap_process(task_id, REST_SERVER, REST_PORT)

    r = requests.get(taks_view_url)
    while (r.json()["task"]["status"] != "reported"):
        time.sleep(10)
        time_flag += 10
        if time_flag > timeout:
            return      # no cuckoo report result
        r = requests.get(taks_view_url)

    sample.cuckoo_tag = get_cuckoo_tag(task_id, REST_SERVER, REST_PORT)


def run():
    """ run the analysis about the sample file.
    """
    
    WORK_PATH = os.getcwd()
    submit_time = time.time()
    
    logger.info('Working path is %s' % (WORK_PATH))

    # to connet to database to store process.
    init_db()

    # to get the cuckoo connection infos
    cuckoo_conf_parser = ConfigParser.ConfigParser()
    cuckoo_conf_parser.read('cuckoo.conf')

    REST_SERVER = cuckoo_conf_parser.get("cuckoo", "REST_SERVER")
    REST_PORT = cuckoo_conf_parser.get("cuckoo", "REST_PORT")
    timeout = cuckoo_conf_parser.get("cuckoo", "timeout")

    # directory of storage of sample and process results 
    if 'samples' not in os.listdir(WORK_PATH):
        os.mkdir('samples')

    # decription of the sample submitted
    sample_conf = ConfigParser.ConfigParser()
    sample_conf.read('sample.info')
    
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
        file_size = len(file_data)

    # anlayze the sample
    sample_Nm = Sample.where().count()
    if sample_Nm > 0 and Sample.where(file_MD5 = file_md5).count() > 0:
        logger.info('File %s has analyzed with md5: %s' % (sample_conf_name, file_md5))
        return
    else:
        sample = Sample()
        
        sample.id = sample_Nm
        sample.file_MD5 = file_md5
        sample.file_path = sample_conf_path
        sample.file_name = sample_conf_name
        sample.file_size = file_size
        sample.submit_t  = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(submit_time))
        sample.mal_type = sample_conf_type
        sample.mal_tag = sample_conf_tag
        sample.mal_desc = sample_conf_desc
        sample.task_id = -1
        sample.cuckoo_tag = ''

        sub_path = str(int(submit_time))+'_'+file_md5
        sample.sample_path = '%s/samples/%s/files' % (WORK_PATH, sub_path)
        sample.log_path = '%s/samples/%s/logs' % (WORK_PATH, sub_path)

       
        os.makedirs(sample.sample_path)        # path ./files to keep the sample
        os.makedirs(sample.log_path)           # path ./logs to keep the results
    
        shutil.copy(sample_conf_path+'/'+sample.file_name, sample.sample_path)
        logger.info('File %s has been copied to %s' % (sample.file_name, sample.sample_path))

        if not sample.mal_type:
            shutil.copy(sample_conf_path+'/'+sample.file_name, sample.log_path)
            os.chdir(sample.log_path)
            os.system('bro -r *.pcap local')
            sample.save()    # save sample information to database

            logger.info('File %s processed, bro logs are in %s' % (sample.file_name, sample.log_path))
        else:
            process(sample, REST_SERVER, REST_PORT, timeout)
            sample.save()
            logger.info('File %s processed, bro logs are in %s' % (sample.file_name, sample.log_path))

    return 


def main():
    """ get malware network behavior from cuckoo and transfer pcap to log
    """

    run()
    
if __name__ == "__main__":
    main()