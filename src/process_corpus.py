# -*- encoding:utf-8 -*-
import os
import re
import codecs
from utility import *
from commons import *


def process_raw_corpus(corpus_list, output_corpus_file):
    outputs = []
    f_out = codecs.open(output_corpus_file, 'w', encoding='utf8')
    for filename in corpus_list:
        print filename
        filepath = os.path.join(raw_corpus_path, filename)
        f_in = codecs.open(filepath, 'r', encoding='utf8')
        while True:
            line = f_in.readline()
            if not line:
                break
            title = line.strip()
            line = f_in.readline()
            sents = []
            while True:
                line = f_in.readline().strip()
                if not line:
                    break
                sents += [sent for sent in re.split(punc, line) if sent]
            outputs += sents
            output_line = title + ' | ' + ' '.join(sents) + '\n'
            f_out.write(output_line)


def process_corpus(input_file, output_gram_file, output_file):
    f_in = codecs.open(input_file, 'r', encoding='utf8')
    lines = f_in.readlines()
    f_in.close()

    f_out = codecs.open(output_gram_file, 'w', encoding='utf8')
    lines_len = len(lines)

    for line in lines:
        sents = line.split(' | ')[1].split(' ')
        sents_len = len(sents)
        if sents_len % 2 != 0:
            continue

        for i in range(0, sents_len, 2):
            if len(sents[i]) == len(sents[i+1]) and len(sents[i]) > 2 and len(sents[i+1])> 2:
                if sents[i][len(sents[i])-1] != u'\n':
                    f_out.write(sents[i] + '\n')
                else:
                    f_out.write(sents[i])

                if sents[i+1][len(sents[i+1])-1] != u'\n':
                    f_out.write(sents[i+1] + '\n')
                else:
                    f_out.write(sents[i+1])

    f_out.close()

    f_in = codecs.open(output_gram_file, 'r', encoding='utf8')
    lines = f_in.readlines()
    lines_len = len(lines)
    f_in.close()

    f_out = codecs.open(output_file, 'w', encoding='utf8')
    for i in range(0, lines_len, 2):
        if len(lines[i]) == len(lines[i+1]):
            f_out.write(lines[i])
            f_out.write(lines[i+1])
    f_out.close()
