#!/usr/bin/env python

import sys
import re
import numpy as np
from numpy import (log, asarray)
from scipy.special import entr
from bs4 import BeautifulSoup
from bs4 import CData

def get_entropy(pk, base=None):
    """
    @param pk: a probability sequence
    @param base: base for log
    @return: the entropy of the sequence
    """
    pk = asarray(pk)
    pk = 1.0*pk/np.sum(pk, axis=0)

    # caclulate entropy
    vec = entr(pk)

    S = np.sum(vec, axis=0)

    if base is not None:
        S /= log(base)

    return S

def get_probability_sequence(file):
    """
    @param file: the file to be caculated.
    @return: a probability sequence of words.
    """
    word_dic = {}

    soup = BeautifulSoup(open(file))

    #delete comment

    #cdata = CData(" ")
    #comment.replace_with(cdata)

    #with open(file) as fr:
    #for line in soup.get_text():
    text = soup.get_text()
    print text
    s = re.findall(r"\w+", text)
    for i in s:
        if i not in word_dic:
            word_dic[i] = 1
        else:
            word_dic[i] += 1
    print len(word_dic)
    #print word_dic.keys()

    word_values = word_dic.values()
    return [float(i)/sum(word_values) for i in word_values]


def main(argv):
    """
    @param argv:
    @return:
    """
    file = argv[0]
    s = get_probability_sequence(file)
    entropy = get_entropy(s)
    print entropy

if __name__ == "__main__":
    main(sys.argv[1:])