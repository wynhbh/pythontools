import urllib2
import datetime
import sys
import os

def craw():
    now = datetime.datetime.now()
    datestr = now.strftime('%Y.%m.%d')

    req = urllib2.Request('http://data.netlab.360.com/feeds/ek/magnitude.txt')
    response = urllib2.urlopen(req)
    the_page = response.read()

    ips = set()
    domains = set()

    with open("magnitude-" + datestr, 'w') as fw:
        fw.write(the_page)

    with open("magnitude-" + datestr) as fr:
        for i in fr:
            if i.startswith("Magnitude"):
                l = i.strip().split("\t")
                ips.update([l[2]])
                domains.update([l[3]])

    with open("magnitude-ip-" + datestr, 'w') as fw:
        for i in ips:
            fw.write(i + "\n")

    with open("magnitude-domain-" + datestr, 'w') as fw:
        for i in domains:
            fw.write(i + "\n")


def main(argv):
    os.chdir("/home/elasticsearch/wy")
    craw()


if __name__ == "__main__":
    main(sys.argv)
