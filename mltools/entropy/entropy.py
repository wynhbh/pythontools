#!/usr/bin/env python

import sys
import re
import time
import numpy as np
from numpy import (log, asarray)
from scipy.special import entr
from bs4 import BeautifulSoup
from bs4 import CData

def english_words():
    """
    return a english word dictionary
    @return: a string list
    """
    word_list = []
    with open("english_word.txt") as fr:
        for line in fr.readlines():
            word_list.append(line.strip())
    return word_list


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
    no_word_strings = {}
    english_word_list = english_words()

    soup = BeautifulSoup(open(file))

    #delete comment

    #cdata = CData(" ")
    #comment.replace_with(cdata)

    #with open(file) as fr:
    #for line in soup.get_text():
    text = soup.get_text()
    #print text
    s = re.findall(r"\w+", text)
    for i in s:
        if i not in word_dic:
            word_dic[i] = 1
        else:
            word_dic[i] += 1
    print len(word_dic)
    #print word_dic.keys()

    #print(time.)
    """

    for i in word_dic:
        if i not in english_word_list:
            no_word_strings[i] = word_dic[i]
    """

    #strings_values = no_word_strings.values()
    word_values = word_dic.values()
    #return [float(i)/sum(strings_values) for i in strings_values]
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