import sys
import  re
import urllib2
from bs4 import BeautifulSoup

def index_parse(html):
    """
    @param html: a html file to be parsed
    @return: parsed results.
    """

    results = []

    soup = BeautifulSoup(html)
    div = soup.find("div", "content") #case sensitive

    for li in div.find_all("li"):
        a = li.find("a", "main_menu")
        text = a.string
        link = a["href"]
        results.append([link, text])

    return results


def html_parse():
    """
    @return:
    """
    pass


def main(argv):
    """
    @param argv:
    @return:
    """

    url1 = "http://www.malware-traffic-analysis.net/2014/index.html"
    url2 = "http://www.malware-traffic-analysis.net/2015/index.html"
    url3 = "http://www.malware-traffic-analysis.net/2016/index.html"

    index = urllib2.urlopen(url3)
    index_html = index.read()
    results = index_parse(index_html)

    path = "http://www.malware-traffic-analysis.net/2016/"

    fw = open('angler2016','w')
    for i in results:
        if "Angler" in i[1]:
            fw.write(path+i[0]+'\t'+i[1]+'\n')
    fw.close()


if __name__ == "__main__":

    main(sys.argv[1:])