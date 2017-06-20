import sys
from itertools import groupby

def longest_consecutive_number(a):
    return max(sum(1 if i < 2 else 0 for i in g) for k, g in groupby(a))

def get_lcn_with_h(f, h):
    lcn = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split()
            if len(l) > h:
                s = [1 if (x < 2.0) else x for x in map(float, l)]
                n = longest_consecutive_number(s)
                lcn.append([len(l), n])

    with open("longest_consecutive_botop_"+str(h), 'w') as fw:
        for n in lcn:
            fw.write(str(n[0]) + " " + str(n[1]) + '\n')

def get_lcn(f):
    lcn = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split()
            s = [1 if (x < 2.0) else x for x in map(float, l)]
            n = longest_consecutive_number(s)
            lcn.append([len(l), n])

    with open("longest_consecutive_botop", 'w') as fw:
        for n in lcn:
            fw.write(str(n[0]) + " " + str(n[1]) + '\n')


def main(argv):
    f = argv[0]
    if len(argv) > 1:
        h = int(argv[1])
        get_lcn_with_h(f, h)
    else:
        get_lcn(f)

if __name__ == "__main__":
    main(sys.argv[1:])