import json
import sys

script, f, w = sys.argv

with open(w,'w') as fw:
    for i,line in enumerate(open(f,'rU')):
        ls = line.strip().split(',')
        md5 = ls[0]
        dic = {}
        for item in ls[3].split('|'):
            kv = item.split(':')
            dic[kv[0]] = ':'.join(kv[1:])
        fw.write(json.dumps([md5,dic])+'\n')
    