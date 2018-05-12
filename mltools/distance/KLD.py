import numpy as np

def kl_distance(p, q):

    return np.sum(p * np.log(p / q))


def array_process(a, b):

    """
    to process two arrays in order to get union distribution
    @param a:
    @param b:
    @return:
    """

    _a = []
    _b = []
    nps = 0.00001

    s = set(a + b)
    for i in s:
        _a.append(float(a.count(i)) / len(a) + nps)
        _b.append(float(b.count(i)) / len(b) + nps)

    return np.array(_a), np.array(_b)


def kld(a, b):

    _a, _b = array_process(a, b)
    kld = kl_distance(_a, _b)

    return kld


# for test
a = [1, 2, 2, 3]
b = [4, 5, 6]
c = [4, 5, 6]
d = [1, 2, 4, 5]
print kld(a, b)
print kld(b, c)
print kld(a, d)