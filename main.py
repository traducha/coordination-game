# -*- coding: utf-8 -*-
import csv
import glob
import igraph as ig
import logging as log
from matplotlib import pyplot as plt
import numpy as np
import os
import time
import sys


B = 1  # b>0 !!!
PAY_OFF_COMPLEX = {'left': {'left': 1, 'right': 0}, 'right': {'left': -B, 'right': 2}}  # pay_off[mine][co-player]
PAY_OFF_SIMPLE = {'left': {'left': 1, 'right': 0}, 'right': {'left': 0, 'right': 1}}  # pay_off[mine][co-player]
MAX_DIFF_PAY_OFF_COMPLEX = 2 + B
MAX_DIFF_PAY_OFF_SIMPLE = 1


def update_strategy(active_payoff, neighbors, av_degree):
    # unconditional imitation - copy the most succesful neig if he's better
    # the best response - chose the strategy giving the best pay_off at the current situation (compute payoff for both and take the better one)
    # replicator -



def main_loop_async(graph, num_nodes, av_degree, time_steps, pay_off_dict):

    for time_step in range(time_steps):
        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy']
        active_payoff = 0

        for neig in neighbors:
            active_payoff += pay_off_dict[active_payoff][graph.vs(neig)['strategy']]

        graph.vs(active_node)['last_payoff'] = active_payoff

        # update the strategy
        graph.vs(active_node)['strategy'] = update_strategy()



