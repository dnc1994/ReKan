# -*- encoding:utf-8 -*-
import sys
import numpy as np
from hmm import init_model
from viterbi import viterbi
from utility import *
from commons import *

top_k_word = 20
top_k_candidate = 10


def gen_candidates(first_half, hash_leaf, k):
    candidates = [(key, val) for (key, val) in hash_leaf.iteritems() if key not in first_half]
    candidates.sort(key=lambda x: x[1], reverse=True)

    if len(candidates) < k:
        pad = candidates[-1]
        for i in range(len(candidates), k):
            candidates.append(pad)

    candidate_words = np.array([w[0] for w in candidates[:k]])
    candidate_probs = np.array([w[1] for w in candidates[:k]])

    return candidate_words, candidate_probs


def deal_repeat(first_half, second_half):
    length_couplet = second_half.shape[1]
    repeat_tags = np.array([-1] * length_couplet)

    for i in range(1, length_couplet):
        for j in range(i):
            if first_half[i] == first_half[j]:
                repeat_tags[i] = j
                break

    for i in range(len(second_half)):
        for j in range(length_couplet):
            if repeat_tags[j] >= 0:
                second_half[i][j] = second_half[i][repeat_tags[j]]

    return second_half


def gen_couplet(first_half):
    assert type(first_half) == unicode
    couplet_length = len(first_half)
    visible_words = np.array([first_half[i] for i in range (couplet_length)])
    hidden_candidate_words = np.array([u' ' for _ in range(top_k_word*couplet_length)]).reshape(top_k_word, couplet_length)
    output_prob = np.random.rand(top_k_word, couplet_length)
    for i in range(couplet_length):
        key = first_half[i]
        if not output_prob_tree.has_key(key):
            print '%s, Cannot generate couplet' % key
            return ''

        hash_leaf = output_prob_tree[key]
        hidden_candidate_words[:,i], output_prob[:,i] = gen_candidates(first_half, hash_leaf, top_k_word)

    for i in range(couplet_length):
        candidate = u''
        for j in range(top_k_word):
            candidate += hidden_candidate_words[j, i]

    try:
        transition_prob, init_prob = init_model(transition_prob_tree, unigram_freq, hidden_candidate_words, top_k_word)
    except:
        return ''

    optimal_path, prob = viterbi(transition_prob, output_prob, init_prob, [], visible_words, top_k_word, top_k_candidate)
    optimal_path = deal_repeat(first_half, optimal_path)

    results = []
    for i in range(optimal_path.shape[0]):
        result = ''
        for j in range(optimal_path.shape[1]):
            result += hidden_candidate_words[optimal_path[i, j], j]
        print result
        results.append(result)

    return results


def interactive():
    while True:
        first_half = raw_input('Please input the first half of the couplet. Input "q" to leave.\n')
        first_half = first_half.decode("gbk")
        if first_half == u'q':
            sys.exit()
        gen_couplet(first_half)


if __name__ == '__main__':
    transition_prob_tree, output_prob_tree, unigram_freq = load(output_prob_file, unigram_file, bigram_file)
    interactive()
