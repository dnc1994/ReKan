# -*- encoding:utf-8 -*-
import sys
from gen_couplets import gen_couplet
from utility import *
from commons import *


def api_wrap():
    transition_prob_tree, output_prob_tree, unigram_freq = load(output_prob_file, unigram_file, bigram_file)
    # todo: encoding
    first_half = sys.argv[1]
    results = gen_couplet(transition_prob_tree, output_prob_tree, unigram_freq, first_half)
    for result in results:
        print result


if __name__ == '__main__':
    api_wrap()
