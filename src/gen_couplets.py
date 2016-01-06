# -*- encoding:utf-8 -*-
import sys
import re
import math
import numpy as np
import jieba
jieba.set_dictionary('..\\data\\dict.txt')
import jieba.posseg as pseg
import pypinyin
from hmm import init_model
from viterbi import viterbi
from utility import *
from commons import *

top_k_word = 20
top_k_candidate = 20
top_k_output = 5


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


def gen_couplet(transition_prob_tree, output_prob_tree, unigram_freq, first_half):
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
        second_half = ''
        for j in range(optimal_path.shape[1]):
            second_half += hidden_candidate_words[optimal_path[i, j], j]
        score = ranking_function(output_prob_tree, first_half, second_half)
        results.append((score, second_half))


    results = sorted(results, reverse=True)[:top_k_output]
    return results


def ranking_function(output_prob_tree, cx, cy):
    # 平仄
    x_py = pypinyin.pinyin(cx, style=pypinyin.TONE2)
    y_py = pypinyin.pinyin(cy, style=pypinyin.TONE2)
    x_pz = map(lambda i: -1 if int(re.search('\d', i[0]).group(0)) <= 2 else 1, x_py)
    y_pz = map(lambda i: -1 if int(re.search('\d', i[0]).group(0)) <= 2 else 1, y_py)
    pingze_score = sum(map(lambda i, j: i + j == 0, x_pz, y_pz)) / float(len(cx)) + 0.001

    def sigmoid(x):
        return 1 / (1 + math.e ** (-x))

    def pos_eq(x_pos, y_pos):
        return x_pos == y_pos or x_pos in y_pos or y_pos in x_pos

    import operator
    smooth_value = 0.001
    freq_amp = 10 ** math.sqrt(len(cx))

    # 词性
    cx_pos = map(lambda x: zip(*pseg.lcut(x)[0])[0][1], cx)
    cy_pos = map(lambda y: zip(*pseg.lcut(y)[0])[0][1], cy)
    pos_score = reduce(operator.add, map(lambda x, y: float(1)/len(cx) if pos_eq(x, y) else 0, cx_pos, cy_pos))
    pos_score += smooth_value

    # 输出概率
    out_score = reduce(operator.mul, map(lambda x, y: output_prob_tree[x][y] * freq_amp, cx, cy))
    out_score = sigmoid(out_score)
    out_score += smooth_value

    # 整合
    score = pingze_score * out_score * pos_score
    # score = pingze_score * pos_score

    # print 'ranking', cy
    # print 'pingze', pingze_score
    # print 'pos', pos_score
    # print 'freq', out_score

    return score


def interactive(encoding='gbk'):
    transition_prob_tree, output_prob_tree, unigram_freq = load(output_prob_file, unigram_file, bigram_file)
    print 'Specified encoding:', encoding
    while True:
        first_half = raw_input('Please input the first half of the couplet. Input "q" to leave.\n')
        first_half = first_half.decode(encoding)
        if first_half == u'q':
            sys.exit()
        results = gen_couplet(transition_prob_tree, output_prob_tree, unigram_freq, first_half)
        for result in results:
            print result[1], result[0]


if __name__ == '__main__':
    # interactive()
    try:
        encoding = sys.argv[1]
    except:
        encoding='gbk'

    interactive(encoding)
