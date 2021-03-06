import sys
import numpy as np


def entropy_2(A):
    """ entropy with logarithm 2
    @param A:
    @return:
    """
    pa = A / A.sum()
    h = -np.sum(pa * np.log2(pa))
    return h

def get_entropy(l):
    """
    @param l:
    @return:
    """
    lset = set(l)
    pi = []
    for j in lset:
        pi.append(l.count(j))
    npa = np.array(map(float, pi))
    e = entropy_2(npa)

    return e


def get_entropy_without_th(f):
    """
    @param f:
    @param h:
    @return:
    """
    en = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split(" ")
            e = get_entropy(l)
            en.append(e)

    with open(f + "_ens", 'w') as fw:
        for i in en:
            fw.write(str(i) + '\n')


def get_entropy_with_th(f, h):
    """
    @param f:
    @param h:
    @return:
    """
    en = []
    with open(f) as fr:
        for i in fr:
            l = i.strip().split(" ")
            if len(l) > h:
                e = get_entropy(l)
                en.append(e)

    with open(f + "_ens_" + str(h), 'w') as fw:
        for i in en:
            fw.write(str(i) + '\n')

def main(argv):
    """
    @param argv:
    @return:
    """

    f = argv[0]

    if len(argv) > 1:
        h = int(argv[1])
        get_entropy_with_th(f, h)
    else:
        get_entropy_without_th(f)


def test():

    test1 = [1.0, 2.0]
    test2 = [2.0, 3.0]

    print get_entropy(test1)
    print get_entropy(test2)


if __name__ == "__main__":
    # main(sys.argv[1:])
    test()
