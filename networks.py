# -*- coding: utf-8 -*-
import sys
import random
import numpy as np
import igraph as ig

from datetime import datetime

import constants as const
from tools import run_with_time, payoff_matrix


###################################
#      multilayer networks        #
###################################


class MultiNet:

    max_rewiring_tries = 20

    def initialize_single_layer(self):
        if self.av_degree == self.num_nodes - 1:
            return ig.Graph.Full(self.num_nodes, directed=False)
        else:
            return ig.Graph.K_Regular(self.num_nodes, self.av_degree, directed=False, multiple=False)

    def __init__(self, num_nodes=None, av_degree=None, num_layers=None, to_rewire=None, shared_nodes_ratio=None,
                 rewire_first_layer=True):
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

        if to_rewire == 0:
            graph = self.initialize_single_layer()
            self.layers = tuple([graph.copy() for _ in range(num_layers)])
        elif to_rewire == 1:
            self.layers = tuple([self.initialize_single_layer() for _ in range(num_layers)])
        elif 0 < to_rewire < 1:

            edges_to_rewire = to_rewire * self.num_edges
            edges_to_rewire = int(edges_to_rewire) if ((int(edges_to_rewire) % 2) == 0) else int(edges_to_rewire) + 1

            graph = self.initialize_single_layer()

            for i in range(num_layers):

                if i == 0 and not rewire_first_layer:
                    self.layers = self.layers + (graph,)
                    continue

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
            raise ValueError('rewiring probability r must be in the range [0,1]')

    def rewire_links(self, graph, edges_to_rewire):
        rewired = set()
        historical_edges = set(graph.get_edgelist())

        for j in range(int(edges_to_rewire / 2)):
            edge_list = graph.get_edgelist()
            edge_one, edge_two, new_edge_one, new_edge_two = self.get_two_new_edges(edge_list, rewired,
                                                                                    historical_edges)

            graph.delete_edges([edge_one, edge_two])
            graph.add_edges([new_edge_one, new_edge_two])

            rewired = rewired.union({new_edge_one, new_edge_two})
            historical_edges = historical_edges.union({new_edge_one, new_edge_two})
        return graph

    def get_two_new_edges(self, full_edge_list, exclude, historical_edges):
        not_rewired_edge_list = list(set(full_edge_list) - exclude)
        edge_one, edge_two = random.sample(range(len(not_rewired_edge_list)), 2)
        edge_one = not_rewired_edge_list[edge_one]
        edge_two = not_rewired_edge_list[edge_two]

        if len(set(edge_one).union(set(edge_two))) != 4:  # the two edges can't share a node
            return self.get_two_new_edges(full_edge_list, exclude, historical_edges)

        new_edge_one = (min(edge_one[0], edge_two[0]), max(edge_one[0], edge_two[0]))
        new_edge_two = (min(edge_one[1], edge_two[1]), max(edge_one[1], edge_two[1]))

        if new_edge_one in historical_edges or new_edge_two in historical_edges:
            new_edge_one = (min(edge_one[0], edge_two[1]), max(edge_one[0], edge_two[1]))
            new_edge_two = (min(edge_one[1], edge_two[0]), max(edge_one[1], edge_two[0]))

        if new_edge_one in historical_edges or new_edge_two in historical_edges:
            return self.get_two_new_edges(full_edge_list, exclude, historical_edges)

        return edge_one, edge_two, new_edge_one, new_edge_two

    def get_layer(self, index):
        return self.layers[index]

    def update_node(self, node_index, layer_index, trait_name=None, trait_value=None):
        if node_index in self.shared_nodes:
            for g in self.layers:
                g.vs(node_index)[trait_name] = trait_value
        else:
            self.get_layer(layer_index).vs(node_index)[trait_name] = trait_value

    def compute_av_edge_overlap(self):
        count = 0.0
        overlap = 0.0
        for i in range(self.num_layers - 1):
            for j in range(i+1, self.num_layers):
                edge_set_one = set(self.get_layer(i).get_edgelist())
                edge_set_two = set(self.get_layer(j).get_edgelist())
                count += 1.0
                overlap += 1.0 * len(edge_set_one.intersection(edge_set_two)) / self.num_edges
        return overlap / count

    def compute_edge_overlap(self, layer_one, layer_two):
        edge_set_one = set(self.get_layer(layer_one).get_edgelist())
        edge_set_two = set(self.get_layer(layer_two).get_edgelist())
        return 1.0 * len(edge_set_one.intersection(set(edge_set_two))) / len(edge_set_one)


class MultiNetCoordination(MultiNet):

    def __init__(self, layers_config=None, payoff_type=None, left_prob=0.5, **kwargs):
        super().__init__(**kwargs)
        self.payoff_dicts = ()
        self.payoff_norms = ()

        if len(layers_config) != len(self.layers):
            raise ValueError(f"layers_config (len={len(layers_config)}) must contain a configuration"
                             f"for each layer (layers={len(self.layers)})!")

        for i in range(self.num_layers):
            self.get_layer(i).vs()['last_payoff'] = None  # to raise an error if it's not updated

            conf = layers_config[i]
            payoff_dict, payoff_norm = payoff_matrix(payoff_type, b=conf['b'], R=conf['R'], P=conf['P'], T=conf['T'],
                                                     S=conf['S'])
            self.payoff_dicts = self.payoff_dicts + (payoff_dict,)
            self.payoff_norms = self.payoff_norms + (payoff_norm,)

            self.get_layer(i)['index_number'] = i
            self.get_layer(i)['payoff_dict'] = payoff_dict
            self.get_layer(i)['payoff_norm'] = payoff_norm
            self.get_layer(i)['layer_config'] = conf

            for node_idx in self.individual_nodes:
                self.get_layer(i).vs(node_idx)['shared'] = False
                if np.random.random() < left_prob:
                    self.get_layer(i).vs(node_idx)['strategy'] = const.LEFT
                    self.get_layer(i).vs(node_idx)['color'] = const.REDISH
                else:
                    self.get_layer(i).vs(node_idx)['strategy'] = const.RIGHT
                    self.get_layer(i).vs(node_idx)['color'] = const.BLUE

        for node_idx in self.shared_nodes:
            if np.random.random() < left_prob:
                self.update_node(node_idx, 0, trait_name='shared', trait_value=True)
                self.update_node(node_idx, 0, trait_name='strategy', trait_value=const.LEFT)
                self.update_node(node_idx, 0, trait_name='color', trait_value=const.REDISH)
            else:
                self.update_node(node_idx, 0, trait_name='shared', trait_value=True)
                self.update_node(node_idx, 0, trait_name='strategy', trait_value=const.RIGHT)
                self.update_node(node_idx, 0, trait_name='color', trait_value=const.BLUE)


##############################
#      simpler graphs        #
##############################


def initialize_random_reg_net(num_nodes, av_degree, erdos=False, payoff_type=None, b=None, R=None, P=None, T=None, S=None):
    if av_degree == num_nodes - 1:
        graph = ig.Graph.Full(num_nodes, directed=False)
    else:
        if not erdos:
            graph = ig.Graph.K_Regular(num_nodes, av_degree, directed=False, multiple=False)
        else:
            graph = ig.Graph.Erdos_Renyi(num_nodes, m=int((av_degree*num_nodes)/2), directed=False, loops=False)

    payoff_dict, payoff_norm = payoff_matrix(payoff_type, b=b, R=R, P=P, T=T, S=S)
    graph['payoff_dict'] = payoff_dict
    graph['payoff_norm'] = payoff_norm
    graph['layer_config'] = {"b": b, "R": R, "P": P, "S": S, "T": T}

    graph.vs()['last_payoff'] = None  # to raise an error if it's not updated
    graph.vs()['strategy'] = const.LEFT
    graph.vs()['color'] = const.REDISH

    for node_idx in random.sample(range(num_nodes), int(num_nodes/2)):
        graph.vs(node_idx)['strategy'] = const.RIGHT
        graph.vs(node_idx)['color'] = const.BLUE

    return graph


##############################
#           tests            #
##############################


@run_with_time
def main():
    # g = initialize_random_reg_net(100, 8)
    # ig.plot(g)

    layers_config = [{"b": None, "R": 1, "P": 0, "S": 1, "T": 2}, {"b": None, "R": 1, "P": 0, "S": 3, "T": 4}]
    net = MultiNetCoordination(num_nodes=1000, av_degree=8, num_layers=2, to_rewire=0.5, shared_nodes_ratio=0.5,
                               rewire_first_layer=False, payoff_type=const.GENERIC, layers_config=layers_config)
    layout = ig.Graph.layout(net.layers[0])
    # for i in range(net.num_layers):
    #     ig.plot(net.layers[i], layout=layout)
    # print(len(net.shared_nodes))
    # print(len(net.individual_nodes))
    print(net.compute_av_edge_overlap())
    print(net.compute_edge_overlap(0, 1))
    print(net.layers[1]['index_number'])


if __name__ == '__main__':
    main()




