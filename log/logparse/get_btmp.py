#!/usr/bin/env python

import sys
import os
import re

def main(argv):


    sp = argv[0]    #sudo password
    des_file = './btmp'  #destination file to record btmp log
    begindir = "/var/log/"
    backup = []

    p = re.compile(r'btmp*')

    for root, dirs, files in os.walk(begindir):
        for file in files:
            match = re.match(p, file)
            if match:
                backup.append(begindir+file)

    #copy btmp to a file
    command = 'echo '+sp+'|sudo -S lastb > '+des_file
    os.system(command)


if __name__ == "__main__":
    main(sys.argv[1:])