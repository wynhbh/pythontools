import os
import sys
from urlparse import urlparse
import MySQLdb
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("main")

def get_http_logs():

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'cuckoo',
        'passwd': 'analysis',
        'db': 'mal_traffic'
    }

    conn = MySQLdb.connect(**db_config)
    cur = conn.cursor()

    #search http logs
    #sql_str = "select log_path from samples where id > 0"

    sql_str = "select log_path from samples  where file_name like '%Angler-%' and file_name not like '%payload%' order by id"

    httpfiles = []

    try:
        cur.execute(sql_str)
        results = cur.fetchall()
        for row in results:
            httpfiles.append(row[0])


    except:
        logger.error("Error: unable to fecth data")
    conn.close()

    return httpfiles

def analysis(N):
    """ analysis values of different fields.
    :param N : index of fields to be analyzed.
    """

    http_log_paths = get_http_logs()

    httplogs = []

    for path in http_log_paths:
        file = path+'/http.log'
        if os.path.isfile(file):
            httplogs.append(file)
        else:
            pass #print(path)

    fields = []

    for log in httplogs:
        with open(log) as f:
            lines = f.readlines()
            rows = len(lines)
            filesize = sum([len(line) for line in lines])

            tss = [] # time series
            methods = []
            uris = []
            uas = []
            request_body_lens = []
            response_body_lens = []
            status_codes = []
            filenames = []

            tmp = []

            for line in lines[8:len(lines)-1]:
                fs = line.strip().split('\t')

                """
                ts = fileds[0]
                uid = fileds[1]
                orig_h = fileds[2]
                orig_p = fileds[3]
                resp_h = fileds[4]
                resp_p = fileds[5]
                trans_depth = fileds[6]
                method = fileds[7]
                host = fileds[8]
                uri = fileds[9]
                referrer = fileds[10]
                user_agent = fileds[11]
                request_body_len = fileds[12]
                response_body_len = fileds[13]
                status_code = fileds[14]
                status_msg = fileds[15]
                info_code = fileds[16]
                info_msg = fileds[17]
                filename = fileds[18]
                tags = fileds[19]
                username = fileds[20]
                password = fileds[21]
                proxied = fileds[22]
                orig_fuids = fileds[23]
                orig_mime_types = fileds[24]
                resp_fuids = fileds[25]
                resp_mime_types = fileds[26]

                tss.append(ts)
                methods.append(method)
                uris.append(uri)
                uas.append(user_agent)
                request_body_lens.append(request_body_len)
                response_body_lens.append(response_body_len)
                status_codes.append(status_code)
                filenames.append(filename)
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


    """
    col = []
    for i in fields:
        for j in i:
            col.append(j)
    print('%s' % ' '.join(map(str,col)))
    """


    """
    dic = {}
    for i in fields:
        for j in i:
            sub = j.split('.')
            if sub[0] in dic:
                dic[sub[0]] += 1
            else:
                dic[sub[0]] = 1


            if len(sub) > 1:
                if sub[-2]+'.'+sub[-1] in dic:
                    dic[sub[-2]+'.'+sub[-1]] += 1
                else:
                    dic[sub[-2]+'.'+sub[-1]] = 1


    ls = sorted(dic.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    for i in range(len(ls)):
        print('%s\t%s' % (ls[i][0], ls[i][1]))
        # print('%s' % join(ls[i][1]))

    """


def main(n):
    analysis(int(n))

if __name__ == "__main__":
    main(sys.argv[1])
