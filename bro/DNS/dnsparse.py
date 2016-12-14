import os
import sys
from urlparse import urlparse
import MySQLdb
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("main")

def analysis(file):
    """ analysis values of different fields.
    :param file : dns file to be analyzed.
    """

    fields = []

    with open(file) as f:
        lines = f.readlines()
        rows = len(lines)
        filesize = sum([len(line) for line in lines])

        tmp = []

        for line in lines[8:len(lines)-1]:
            fs = line.strip().split('\t')

            """
            fields:
            ts
            uid
            id.orig_h
            id.orig_p
            id.resp_h
            id.resp_p
            proto
            trans_id
            query
            qclass
            qclass_name
            qtype
            qtype_name
            rcode
            rcode_name
            AA
            TC
            RD
            RA
            Z
            answersTTLs
            rejected
            """

            tmp.append(fs[N])

        #print(log, rows, ','.join(methods))

        # time intervals
        #tss_sorted = sorted(map(float,tmp))
        #tss_sorted = map(float, tmp)
        #intervals = map(int,[tss_sorted[i+1]-tss_sorted[i] for i in range(len(tss_sorted)-1)])
        #print('%s %s' % (log, ' '.join(map(str,intervals))))
            #file = urlparse(fs[N]).path.split('/')[-1].split('.')
            #if len(file)>1:
            #   tmp.append(file[-1])
            #tmp.append(urlparse(fs[N]).path.split('/')[-1])
            #tmp.append(urlparse(fs[N]).path)

        #fields.append(set(tmp))
        #fields.append(intervals)
        fields.append(tmp)


    dic = {}
    for i in fields:
        for j in i:
            if j in dic:
                dic[j] += 1
            else:
                dic[j] = 1
    ls = sorted(dic.items(), lambda x,y: cmp(x[1], y[1]), reverse = True)
    for i in range(len(ls)):
        print('%s\t%s' %(ls[i][0], ls[i][1]))
        #print('%s' % join(ls[i][1]))

def main(n):
    analysis(int(n))

if __name__ == "__main__":
    main(sys.argv[1])
