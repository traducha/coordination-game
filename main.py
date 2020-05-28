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
        self.shared_nodes = tuple(np.random.randint(0, num_nodes, int(shared_nodes_ratio * num_nodes)))
        self.layers = ()

        sys.setrecursionlimit(10000)

        if to_rewire > 1:
            raise ValueError('rewiring probability r must be in the range [0,1]')
        elif to_rewire > 0:
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
        else:
            for i in range(num_layers):
                self.layers = self.layers + (graph.copy(),)

        sys.setrecursionlimit(1000)

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
        # print(edge_list)
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


def compute_edge_overlap(graph_one, graph_two):
    edge_list_one = graph_one.get_edgelist()
    return len(set(edge_list_one).intersection(set(graph_two.get_edgelist()))) / len(edge_list_one)


if __name__ == '__main__':
    net = MultiNet(50, 20, 3, 1, 0.5)
    print(net)
    print(net.layers)
    layout = ig.Graph.layout(net.layers[0])
    # ig.plot(net.layers[0], layout=layout)
    # ig.plot(net.layers[1], layout=layout)
    # ig.plot(net.layers[2], layout=layout)
    print(compute_edge_overlap(net.layers[0], net.layers[1]))
    print(compute_edge_overlap(net.layers[2], net.layers[1]))
    print(net.shared_nodes_ratio)



# network initialization - random regular lattice
# allow node overlap - nodes are just indexed, for every node keep the list of groups of layers that are connected
# e.g [(1,2), (3,4), 5] - layers 1 and 2 are connected and 3 and 4, but 5 is separate from all
# allow any edge overlap (at first for 2 layers) - start with identical nets and rewire a certain fraction of links
# allow an arbitrary number of layers in simulations


# game played pay-off matrix
# cooperation game with b><1
# 1,1   0,-b
# -b,0  2,2

# update dynamics and evalution of the strategy
# player looks at all neighbors in one of the layers (random one, always one, both at once?)
# and chooses the best strategy, i.e. the highest payoff last round (if the pay-off is bigger than his)
# synchronous update (?) everyone plays with all the neigs on all layers and then update strategies and then reset gains
# or one by one?




