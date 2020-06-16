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


class MultiNet:

    max_rewiring_tries = 20

    def __init__(self, num_nodes, av_degree, num_layers, to_rewire, shared_nodes_ratio):
        graph = ig.Graph.K_Regular(num_nodes, av_degree, directed=False, multiple=False)
        self.num_nodes = num_nodes
        self.av_degree = av_degree
        self.num_edges = int(num_nodes * av_degree / 2)
        self.num_layers = num_layers
        self.rewired_fraction = to_rewire
        self.shared_nodes_ratio = shared_nodes_ratio
        self.shared_nodes = tuple(
            [int(i) for i in np.random.choice(num_nodes, size=round(shared_nodes_ratio * num_nodes), replace=False)])
        self.individual_nodes = tuple({i for i in range(self.num_nodes)}.difference(set(self.shared_nodes)))
        self.layers = ()

        if to_rewire > 1:
            raise ValueError('rewiring probability r must be in the range [0,1]')
        elif to_rewire > 0:
            sys.setrecursionlimit(10000)

            edges_to_rewire = to_rewire * self.num_edges
            edges_to_rewire = int(edges_to_rewire) if ((int(edges_to_rewire) % 2) == 0) else int(edges_to_rewire) + 1

            for i in range(num_layers):
                new_graph = graph.copy()
                done = False
                for e in range(self.max_rewiring_tries):
                    try:
                        new_graph = self.rewire_links(new_graph, edges_to_rewire)
                        done = True
                        break
                    except RecursionError:
                        print('RecursionError in MultiNet __init__ silenced')
                        continue
                if not done:
                    raise RecursionError('too many tries to rewire links')

                self.layers = self.layers + (new_graph,)

            sys.setrecursionlimit(1000)
        else:
            for i in range(num_layers):
                self.layers = self.layers + (graph.copy(),)

    def rewire_links(self, graph, edges_to_rewire):
        rewired = set()
        for j in range(int(edges_to_rewire / 2)):
            edge_list = graph.get_edgelist()
            edge_one, edge_two, new_edge_one, new_edge_two = self.get_two_new_edges(edge_list, rewired)

            graph.delete_edges([edge_one, edge_two])
            graph.add_edges([new_edge_one, new_edge_two])

            rewired = rewired.union({new_edge_one, new_edge_two})
        return graph

    def get_two_new_edges(self, edge_list, exclude):
        edge_list = list(set(edge_list) - exclude)
        edge_one, edge_two = np.random.randint(0, len(edge_list), 2)
        edge_one = edge_list[edge_one]
        edge_two = edge_list[edge_two]

        new_edge_one = (min(edge_one[0], edge_two[0]), max(edge_one[0], edge_two[0]))
        new_edge_two = (min(edge_one[1], edge_two[1]), max(edge_one[1], edge_two[1]))
        if new_edge_one in edge_list or new_edge_two in edge_list or new_edge_one[0] == new_edge_one[1] or \
                        new_edge_two[0] == new_edge_two[1] or new_edge_one in exclude or new_edge_two in exclude:
            new_edge_one = (min(edge_one[0], edge_two[1]), max(edge_one[0], edge_two[1]))
            new_edge_two = (min(edge_one[1], edge_two[0]), max(edge_one[1], edge_two[0]))
        if new_edge_one in edge_list or new_edge_two in edge_list or new_edge_one[0] == new_edge_one[1] or \
                        new_edge_two[0] == new_edge_two[1] or new_edge_one in exclude or new_edge_two in exclude:
            return self.get_two_new_edges(edge_list, exclude)

        return edge_one, edge_two, new_edge_one, new_edge_two

    def compute_av_edge_overlap(self):
        count = 0.0
        overlap = 0.0
        for i in range(self.num_layers - 1):
            for j in range(i+1, self.num_layers):
                edge_set_one = set(self.layers[i].get_edgelist())
                edge_set_two = set(self.layers[j].get_edgelist())
                count += 1.0
                overlap += 1.0 * len(edge_set_one.intersection(edge_set_two)) / self.num_edges
        return overlap / count


class MultiNetCoordination(MultiNet):

    def __init__(self, *args, left_prob=0.5):
        super().__init__(*args)

        for i in range(self.num_layers):
            for node_idx in self.individual_nodes:
                self.layers[i].vs(node_idx)['shared'] = False
                if np.random.random() < left_prob:
                    self.layers[i].vs(node_idx)['strategy'] = 'left'
                    self.layers[i].vs(node_idx)['color'] = 'blue'
                else:
                    self.layers[i].vs(node_idx)['strategy'] = 'right'
                    self.layers[i].vs(node_idx)['color'] = 'orange'

        for node_idx in self.shared_nodes:
            if np.random.random() < left_prob:
                for i in range(self.num_layers):
                    self.layers[i].vs(node_idx)['shared'] = True
                    self.layers[i].vs(node_idx)['strategy'] = 'left'
                    self.layers[i].vs(node_idx)['color'] = 'blue'
            else:
                for i in range(self.num_layers):
                    self.layers[i].vs(node_idx)['shared'] = True
                    self.layers[i].vs(node_idx)['strategy'] = 'right'
                    self.layers[i].vs(node_idx)['color'] = 'orange'


def compute_edge_overlap(graph_one, graph_two):
    edge_set_one = set(graph_one.get_edgelist())
    edge_set_two = set(graph_two.get_edgelist())
    return 1.0 * len(edge_set_one.intersection(set(edge_set_two))) / len(edge_set_one)


##############################
#      simpler graphs        #
##############################


def initialize_random_reg_net(num_nodes, av_degree, left_prob=0.5):
    graph = ig.Graph.K_Regular(num_nodes, av_degree, directed=False, multiple=False)
    for node_idx in range(num_nodes):
        graph.vs(node_idx)['last_payoff'] = 0
        if np.random.random() < left_prob:
            graph.vs(node_idx)['strategy'] = 'left'
            graph.vs(node_idx)['color'] = 'blue'
        else:
            graph.vs(node_idx)['strategy'] = 'right'
            graph.vs(node_idx)['color'] = 'orange'
    return graph


if __name__ == '__main__':
    g = initialize_random_reg_net(100, 8)
    ig.plot(g)


    # net = MultiNetCoordination(10, 4, 6, 1, 0.0)
    # layout = ig.Graph.layout(net.layers[0])
    # for i in range(net.num_layers):
    #     ig.plot(net.layers[i], layout=layout)
    # print(net.shared_nodes)
    # print(net.individual_nodes)
    # print(net.compute_av_edge_overlap())
    # print(net.shared_nodes_ratio)





# game played pay-off matrix
# coordination game game with b><1
# 1,1   0,-b
# -b,0  2,2
b = 1
pay_off = {'left': {'left': 1, 'right': 0}, 'right': {'left': -b, 'right': 2}}  # pay_off[mine][co-player]
pay_off_simple = {'left': {'left': 1, 'right': 0}, 'right': {'left': 0, 'right': 1}}  # pay_off[mine][co-player]

# update dynamics and evalution of the strategy
# player looks at all neighbors in one of the layers (random one, always one, both at once?)
# and chooses the best strategy, i.e. the highest payoff last round (if the pay-off is bigger than his)
# synchronous update (?) everyone plays with all the neigs on all layers and then update strategies and then reset gains
# or one by one?




