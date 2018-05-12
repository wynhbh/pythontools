
def element_count(a):
    """
    @param a: input array
    @return: an array of sorted element with counts
    """

    s = set(a)
    t = {}
    for i in s:
        t[i] = a.count(i)

    ls = sorted(t.items(), lambda x, y: cmp(x[1] > y[1]), reverse=True)

    return ls
