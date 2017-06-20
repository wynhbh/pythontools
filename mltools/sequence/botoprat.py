import sys
from itertools import groupby

def rat(a):

    return float([1 if (g<2) else g for g in (a)].count(1))/len(a)

def get_rat_with_h(f, h):
    rats = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split()
            if len(l) > h:
                s = map(float, l)
                n = rat(s)
                rats.append([len(l), n])

    with open("botoprat_"+str(h), 'w') as fw:
        for n in rats:
            fw.write(str(n[0]) + " " + str(n[1]) + '\n')

def get_rat(f):
    rats = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split()
            s = map(float, l)
            n = rat(s)
            rats.append([len(l), n])

    with open("botoprat", 'w') as fw:
        for n in rats:
            fw.write(str(n[0]) + " " + str(n[1]) + '\n')


def main(argv):
    f = argv[0]
    if len(argv) > 1:
        h = int(argv[1])
        get_rat_with_h(f, h)
    else:
        get_rat(f)

if __name__ == "__main__":
    main(sys.argv[1:])