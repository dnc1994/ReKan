# -*- encoding:utf-8 -*-
from __future__ import division
import sys
import numpy as np
from utility import *
from commons import *


def init_model(transition_prob_tree, unigram_dict, hidden_candidate_words, top_k_word):
    init_prob = calc_init_prob(unigram_dict, hidden_candidate_words[:, 0])
    hidden_transition_matrix = gen_hidden_transition_matrix(transition_prob_tree, unigram_dict, hidden_candidate_words, top_k_word)
    return hidden_transition_matrix, init_prob


def calc_init_prob(unigram_dict, initial_words):
    word_num = len(initial_words)
    init_prob = np.random.rand(word_num)

    total_count = 0
    for word in initial_words:
        total_count += unigram_dict[word]

    for index, word in enumerate(initial_words):
        init_prob[index] = unigram_dict[word] / float(total_count)

    return init_prob


def calc_transfer_prob(unigram_freq, bigram_freq, word_pairs_freq, transition_prob_file, output_prob_file):
    f_out = codecs.open(transition_prob_file, 'w', encoding='utf8')
    for key in bigram_freq.keys():
        [first_word, _] = key.split(' ')
        try:
            unigram_count = unigram_freq[first_word]
            bigram_count = bigram_freq[key]
        except:
            raise
        f_out.write(u'{0} {1}\n'.format(key, bigram_count / float(unigram_count)))
    f_out.close()

    f_out = codecs.open(output_prob_file, 'w', encoding='utf8')
    for key in word_pairs_freq.keys():
        [first_word, second_word] = key.split(" ")
        try:
            first_word_count = unigram_freq[first_word]
            second_word_count = unigram_freq[second_word]
            word_pairs_count = word_pairs_freq[key]

            transfer_prob = word_pairs_count / float(first_word_count)
            f_out.write(u'{0} {1} {2}\n'.format(first_word, second_word, transfer_prob))

            if first_word != second_word:
                backward_transfer_pro = word_pairs_count / float(second_word_count)
                f_out.write(u'{0} {1} {2}\n'.format(second_word, first_word, backward_transfer_pro))

        except:
            raise
    f_out.close()


def gen_hidden_transition_matrix(transition_prob_tree, unigram_dict, hidden_candidate_words, top_k_word):
    state_num = hidden_candidate_words.shape[1]
    hidden_transfer_matrix = np.random.rand(state_num-1, top_k_word, top_k_word)

    for i in range(state_num-1):
        for j in range(top_k_word):
            start_word = hidden_candidate_words[j, i]
            end_words = hidden_candidate_words[:, i+1]
            unigram = unigram_dict[start_word]
            try:
                hash_leaf = transition_prob_tree[start_word]
            except:
                print 'key not exist in inner transfer tree'
                raise

            bigram = np.array([0] * top_k_word)
            for (index, word) in enumerate(end_words):
                bigram[index] = hash_leaf.get(word, 0)

            hidden_transfer_matrix[i, j, :] = additive_smooth(bigram, unigram)

    return hidden_transfer_matrix
