# -*- encoding:utf-8 -*-
from process_corpus import process_raw_corpus, process_corpus
from hmm import calc_transfer_prob
from utility import *
from commons import *


def train():
    process_raw_corpus(corpus_list, full_corpus_file)
    process_corpus(full_corpus_file, train_corpus_gram_file, train_corpus_file)
    unigram_freq = count_ngrams([train_corpus_file], unigram_file, 1)
    bigram_freq = count_ngrams([train_corpus_file], bigram_file, 2)
    word_pairs_freq = count_word_pairs([train_corpus_file], word_pairs_file)
    calc_transfer_prob(unigram_freq, bigram_freq, word_pairs_freq, inner_transfer_file, intra_transfer_file)


if __name__ == '__main__':
    train()
