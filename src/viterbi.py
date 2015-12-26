# -*- encoding:utf-8 -*-
import numpy as np
from utility import *
from commons import *

def viterbi(hidden_transition, hidden_visible_transition, init_prob, hidden_candidate_words, visible_words, top_k_words, top_k_candidates=1):
    state_num = len(visible_words)
    state_prob_matrix = np.random.rand(top_k_words, state_num)
    state_optimal_path = np.array([0 for _ in range((state_num+1)*top_k_words)], dtype='i').reshape(top_k_words, state_num+1)
    optimal_path = np.array([0 for _ in range(state_num*top_k_candidates)], dtype='i').reshape(top_k_candidates, state_num)
    max_prob = np.array([0 for _ in range(top_k_candidates)], dtype='i')

    state_prob_matrix[:, 0] = init_prob[:] * hidden_visible_transition[:,0]

    for i in range(0, state_num-1):
        state_prob_matrix[:, i+1] = np.max(state_prob_matrix[:,i].reshape(-1, 1) * hidden_transition[i, :, :] * hidden_visible_transition[:, i+1], 0)
        state_optimal_path[:, i+1] = np.argmax(state_prob_matrix[:,i].reshape(-1, 1) * hidden_transition[i, :, :] * hidden_visible_transition[:, i], 0)

    state_optimal_path[:,-1] = [i for i in range(top_k_words)]
    max_last_word_index = np.argmax(state_prob_matrix[:,state_num-1])
    max_prob = state_prob_matrix[max_last_word_index, state_num-1]

    last_prob_temp = np.copy(state_prob_matrix[:, state_num-1])
    last_prob = last_prob_temp.tolist()
    index_last_prob = []
    for i in range(len(last_prob)):
        index_last_prob.append([last_prob[i], i])
    index_last_prob.sort(key = lambda x: x[0], reverse=True)

    for i in range(top_k_candidates):
        optimal_path[i, state_num-1] = state_optimal_path[index_last_prob[i][1], state_num]
        word_index = state_optimal_path[index_last_prob[i][1], state_num]
        for j in range(state_num-1, 0, -1):
            optimal_path[i, j-1] = state_optimal_path[word_index, j]
            word_index = optimal_path[i, j-1]

    return optimal_path, max_prob
