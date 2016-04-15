
import sys
import requests
import json

script, task_id = sys.argv

REST_SERVER = "10.10.4.229"
REST_PORT = "5455"

REST_REPORT_URL = 'http://%s:%s/tasks/report/' % (REST_SERVER, REST_PORT)

report_url = REST_REPORT_URL + task_id

report = requests.get(report_url).json()

# test
print(report)

av_res = {}

ants = [u'Avast', u'Microsoft', u'AVG', u'Avira', u'Symantec', u'McAfee', u'ESET-NOD32', u'Kaspersky', u'Comodo',
        u'BitDefender', u'Bkav', u'MicroWorld-eScan', u'nProtect', u'CAT-QuickHeal', u'Malwarebytes', u'VIPRE',
        u'AegisLab', u'TheHacker', u'K7GW', u'K7AntiVirus', u'Agnitum', u'F-Prot', u'TrendMicro-HouseCall', u'ClamAV',
        u'Alibaba', u'NANO-Antivirus', u'SUPERAntiSpyware', u'ByteHero', u'Rising', u'Ad-Aware', u'Sophos', u'F-Secure',
        u'DrWeb', u'Zillya', u'TrendMicro', u'McAfee-GW-Edition', u'Emsisoft', u'Cyren', u'Jiangmin', u'Antiy-AVL',
        u'Kingsoft', u'Arcabit', u'ViRobot', u'AhnLab-V3', u'GData', u'TotalDefense', u'ALYac', u'AVware', u'VBA32',
        u'Panda', u'Zoner', u'Tencent', u'Ikarus', u'Fortinet', u'Baidu-International', u'Qihoo-360']


if "response_code" in report["virustotal"] and report["virustotal"]["response_code"] == 1:
    for av in report["virustotal"]["scans"]:
        if report["virustotal"]["scans"][av]["detected"]:
            av_res[av] = report["virustotal"]["scans"][av]["result"]
else:
    print('no virustotal responses')

cuckoo_tags = []

for i in ants:
    if i in av_res:
        cuckoo_tags.append("%s %s"%(i, av_res[i]))
    if len(cuckoo_tags)>2:
        break

for i in cuckoo_tags:
    print(i)