#!/usr/bin/env python

"""
save successed logins
"""


import sys
import os
import re
import time


def main(argv):

    des_file = './wtmp'  # destination file to record wtmp log
    tmp_file = 'tmp_wtmp'
    begindir = "/var/log/"
    backup = []
    record_f = ''

    p = re.compile(r'wtmp*')

    for root, dirs, files in os.walk(begindir):
        for file in files:
            match = re.match(p, file)
            if match:
                backup.append(begindir + file)

    # copy wtmp to a file
    for file in backup:
        command = 'last -F -w -i -f ' + file + '> ' + tmp_file
        os.system(command)

        if file == '/var/log/wtmp':
            with open(tmp_file) as fr:
                for line in fr:
                    n = sum([1 for i in line.strip().split(' ') if i != ''])
                    if n == 15:
                        record_f = fr.readline()

        with open(des_file, 'a') as fw, open(tmp_file) as fr:
            for line in fr:
                n = sum([1 for i in line.strip().split(' ') if i != ''])
                if n == 15:
                    fw.write(line)

        os.system('rm ' + tmp_file)

    # update new records
    while 1:
        time.sleep(10)
        command = 'last -F -w -i > ' + tmp_file
        os.system(command)

        new_records = []
        with open(tmp_file) as fr:
            for line in fr:
                n = sum([1 for i in line.strip().split(' ') if i != ''])
                if n == 15 and line != record_f:
                    new_records.append(line)
                elif n == 15 and line == record_f:
                    break
                else:
                    pass

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