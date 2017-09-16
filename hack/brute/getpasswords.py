import urllib2
from bs4 import BeautifulSoup
import sys
import time

def get_passwords(page):
    """
    @param page:
    @return: passwords
    """

    pws = []
    soup = BeautifulSoup(page)
    ls = soup.select('#cntContent_lstMain')

    for i in ls:
        for j in i.select('tr'):
            l = j.select('td')
            #if l[0].get_text().isdigit():
            if len(l) > 0:
                pws.append(l[1].get_text())

    return pws





def save(l):

    with open('pws', 'a') as fw:
        for i in l:
            fw.write(str(i) + '\n')


def run():

    for i in range(89, 101):
        page = 'http://www.passwordrandom.com/most-popular-passwords/page/' + str(i)
        print page
        req = urllib2.Request(page)
        response = urllib2.urlopen(req)
        the_page = response.read()
        ps = get_passwords(the_page)
        save(ps)
        time.sleep(10)



def main(argv):

    run()


if __name__=="__main__":
    main(sys.argv[1:])