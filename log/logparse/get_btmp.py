#!/usr/bin/env python

import sys
import os
import re
import time


def record_check(line):
    """
    @param line: a line from wtmp/btmp
    @return: the number of a record item
    """

    c = 0

    rs = line.strip().split(' ')

    for i in rs:
        if i != '':
            c += 1

    return c

    # sum([1 for i in line.strip().split(' ') if i != ''])


def main(argv):


    sp = argv[0]    # sudo password
    des_file = './btmp'  # destination file to record btmp log
    tmp_file = 'tmp_file'
    begindir = "/var/log/"
    backup = []
    record_f = ''

    p = re.compile(r'btmp*')

    for root, dirs, files in os.walk(begindir):
        for file in files:
            match = re.match(p, file)
            if match:
                backup.append(begindir + file)


    if len(backup) > 0:
        command = 'echo ' + sp + '|sudo -S lastb -F -w -i > ' + tmp_file
        os.system(command)

        with open(tmp_file) as fr:
            record_f = fr.readline().strip()

        os.system('rm ' + tmp_file)


    # copy btmp to a file
    for i in backup:
        command = 'echo ' + sp + '|sudo -S lastb -F -w -i -f' + i + '>> ' + des_file
        os.system(command)


    while 1:
        time.sleep(10)
        command = 'echo ' + sp + '|sudo -S lastb -F -w -i > ' + tmp_file
        os.system(command)

        new_records = []
        with open(tmp_file) as fr:
            for line in fr:
                if line.strip() != record_f:
                    new_records.append(line)
                else:
                    break
        # update the record flag
        if new_records != []:
            record_f = new_records[0]

        # save the new records
        with open(des_file, 'a') as fw:
            for i in new_records:
                fw.write(i)

        os.system('rm ' + tmp_file)


if __name__ == "__main__":
    main(sys.argv[1:])