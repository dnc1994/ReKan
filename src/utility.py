# -*- encoding:utf-8 -*-
from __future__ import division
import codecs
from commons import *


def additive_smooth(x, y):
    return (x + 1) / (y + len(x))


def count_ngrams(input_list, output_file, ngram):
    count_table = {}
    for filepath in input_list:
        f_in = codecs.open(filepath, 'r', encoding='utf8')
        lines = f_in.readlines()
        assert len(lines) % 2 == 0
        for line in lines:
            word_num = len(line) - 2
            for j in range(word_num - ngram + 1):
                key = ' '.join(line[j:j+ngram])
                count_table[key] = 1 + count_table.get(key, 1)
        f_in.close()

    f_out = codecs.open(output_file, 'w', encoding='utf8')
    for key in count_table.keys():
        f_out.write(u'{0} {1}\n'.format(key, count_table[key]))
    f_out.close()

    return count_table


def count_word_pairs(input_list, output_file):
    count_table = {}
    for filepath in input_list:
        f_in = codecs.open(filepath, 'r', encoding='utf8')
        lines = f_in.readlines()
        assert len(lines) % 2 == 0
        for i in range(0, len(lines), 2):
            first_sentence = lines[i]
            second_sentence = lines[i+1]
            word_num = len(first_sentence) - 2
            for j in range(word_num):
                try:
                    key_first = first_sentence[j] + ' ' + second_sentence[j]
                    key_second = second_sentence[j] + ' ' + first_sentence[j]
                    if count_table.has_key(key_first):
                        count_table[key_first] += 1
                    elif count_table.has_key(key_second):
                        count_table[key_second] += 1
                    else:
                        count_table[key_first] = 1
                except:
                    raise
        f_in.close()

    f_out = codecs.open(output_file, 'w', encoding='utf8')
    for key in count_table.keys():
        f_out.write(u'{0} {1}\n'.format(key, count_table[key]))
    f_out.close()

    return count_table


def build_hash_dict(hash_dict, word, value):
    if hash_dict.has_key(word):
        raise
    else:
        hash_dict[word] = value


def build_hash_tree_node(hash_tree, first_word, second_word, value):
    if hash_tree.has_key(first_word):
        hash_leaf = hash_tree[first_word]
        if hash_leaf.has_key(second_word):
            raise
        hash_leaf[second_word] = value
    else:
        hash_leaf = {}
        hash_leaf[second_word] = value
        hash_tree[first_word] = hash_leaf


def build_hash_tree(output_prob_lines, unigram_lines, bigram_lines):
    transition_prob_hash_tree = {}
    for line in bigram_lines:
        first_word, second_word, count = line.split(' ')
        build_hash_tree_node(transition_prob_hash_tree, first_word, second_word, int(count))

    output_prob_hash_tree = {}
    for line in output_prob_lines:
        [first_word, second_word, prob] = line.split(' ')
        build_hash_tree_node(output_prob_hash_tree, first_word, second_word, float(prob))

    unigram_freq = {}
    for line in unigram_lines:
        word, count = line.split(' ')
        build_hash_dict(unigram_freq, word, int(count))

    return transition_prob_hash_tree, output_prob_hash_tree, unigram_freq


def load(output_prob_file, unigram_file, bigram_file):
    f_in = codecs.open(output_prob_file, 'r', encoding='utf8')
    output_prob_lines = f_in.readlines()
    f_in.close()

    f_in = codecs.open(unigram_file, 'r', encoding='utf8')
    unigram_lines = f_in.readlines()
    f_in.close()

    f_in = codecs.open(bigram_file, 'r', encoding='utf8')
    bigram_lines = f_in.readlines()
    f_in.close()

    return build_hash_tree(output_prob_lines, unigram_lines, bigram_lines)
