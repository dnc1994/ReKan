# -*- encoding:utf-8 -*-
import numpy as np
from utility import *
from commons import *

def viterbi_decode(hidden_transfer, hidden_visible_transfer, init_prob, hidden_candidate_words, visible_words, top_k_words, top_k_candidates=1):
    state_num = len(visible_words)
    state_prob_matrix = np.random.rand(top_k_words, state_num)
    state_optimal_route = np.array([0 for i in range((state_num+1)*top_k_words)], dtype='i').reshape(top_k_words, state_num+1)
    optimal_path = np.array([0 for i in range(state_num*top_k_candidates)], dtype='i').reshape(top_k_candidates, state_num)
    max_prob = np.array([0 for i in range(top_k_candidates)], dtype="i")

    # 1. Initialization
    state_prob_matrix[:, 0] = init_prob[:] * hidden_visible_transfer[:,0]

    # 2. Recursion
    for i in range(0, state_num-1):
        state_prob_matrix[:, i+1] = np.max(state_prob_matrix[:,i].reshape(-1, 1) * hidden_transfer[i, :, :] * hidden_visible_transfer[:, i+1], 0)
        state_optimal_route[:, i+1] = np.argmax(state_prob_matrix[:,i].reshape(-1, 1) * hidden_transfer[i, :, :] * hidden_visible_transfer[:, i], 0)

    # 3. Find word having max probability
    state_optimal_route[:,-1] = [i for i in range(top_k_words)]
    max_last_word_index = np.argmax(state_prob_matrix[:,state_num-1])
    max_prob = state_prob_matrix[max_last_word_index, state_num-1]

    # 4. Path backtracking
    last_pro_temp = np.copy(state_prob_matrix[:, state_num-1])
    last_pro = last_pro_temp.tolist()
    index_last_pro = []
    for i in range(len(last_pro)):
        index_last_pro.append([last_pro[i], i])
    index_last_pro.sort(key = lambda x: x[0], reverse=True)

    for i in range(top_k_candidates):
        optimal_path[i, state_num-1] = state_optimal_route[index_last_pro[i][1], state_num]
        word_index = state_optimal_route[index_last_pro[i][1], state_num]
        for j in range(state_num-1, 0, -1):
            optimal_path[i, j-1] = state_optimal_route[word_index, j]
            word_index = optimal_path[i, j-1]

    return optimal_path, max_prob
