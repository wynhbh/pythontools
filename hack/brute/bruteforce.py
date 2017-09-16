import urllib2
import urllib
from bs4 import BeautifulSoup
import sys
import time


def get_passwords():
    """
    @param page:
    @return: passwords
    """

    pws = []

    with open('pws') as fr:
        for i in fr:
            pws.append(i.strip())

    return pws



def get_username():
    """
    @param page:
    @return: passwords
    """

    us = []


    for i in range(100):
        username = '2015M8009073' + '%03d' % i
        us.append(username)

    return us


def save(l):

    with open('pws', 'a') as fw:
        for i in l:
            fw.write(str(i) + '\n')


def run():

    pws = get_passwords()
    username = get_username()
    url = 'http://www.douban.com'

    for i in pws:

        info = {'username': 'Michael Foord',
                'password': 'Northampton'}
        data = urllib.urlencode(info)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        if success(the_page):
            save(pws)
        time.sleep(10)



def main(argv):

    run()


if __name__=="__main__":
    main(sys.argv[1:])