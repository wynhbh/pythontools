"""
CCDF from matlab methods


function [nn, x_train] = ccdf_law(x,bin_num)
    [N_train, x_train] = hist(x,bin_num);
    N_train = N_train/(sum(N_train)); %/(x_train(2)-x_train(1));
    nn=N_train;
    aa = 0;
    for i=1:bin_num
        aa = aa + N_train(i);
        nn(i) = 1-aa + N_train(i);
    end
end

"""

def hist(x, bin_num):
    """
    @param x:
    @param bin_num:
    @return: (counts, centers)
    """
    min_x = min(x)
    max_x = max(x)

    inter = (max_x - min_x)/bin_num

    counts = [0] * bin_num

    for i in x:
        j = int((i - min_x)/inter)
        counts[j] += 1

    centers = [(min_x + (0.5 + i) * inter) for i in range(bin_num)]

    return counts, centers


def ccdf(x, bin_num):
    """
    @param x: float set
    @param bin_num:
    @return:
    """

    counts, centers = hist(x, bin_num)

    counts = [float(counts[i])/sum(counts) for i in range(len(counts))]

    a = 0
    nn = []
    for i in range(bin_num):
        nn[i] = 1 - a
        a += counts[i]

    return nn, centers


def test():
    pass