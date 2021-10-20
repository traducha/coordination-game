# -*- coding: utf-8 -*-
import igraph as ig
import numpy as np

from datetime import datetime

import constants as const
from networks import initialize_random_reg_net, MultiNetCoordination
from tools import log


#######################################
#           payoff updates            #
#######################################


def unconditional_imitation(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm, **kwargs):
    # unconditional imitation - copy the most successful neig if he's better
    max_neig_payoff = float('-inf')
    max_neig_strategy = None
    for neig_id, neig_strategy, neig_payoff in neig_list:
        if neig_payoff > max_neig_payoff:
            max_neig_payoff = neig_payoff
            max_neig_strategy = neig_strategy

    if max_neig_payoff > active_payoff:
        return max_neig_strategy
    else:
        return active_strategy


def best_response(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm, **kwargs):
    # the best response - chose the strategy giving the best pay_off at the current situation
    if len(neig_list) == 0:  # ER case for small k
        return active_strategy

    payoff_left = 0
    payoff_right = 0
    for neig_id, neig_strategy, neig_payoff in neig_list:
        payoff_left += pay_off_dict[const.LEFT][neig_strategy]
        payoff_right += pay_off_dict[const.RIGHT][neig_strategy]

    if payoff_left == payoff_right:
        return np.random.choice([const.LEFT, const.RIGHT])
    elif payoff_left > payoff_right:
        return const.LEFT
    else:
        return const.RIGHT


def replicator_dynamics(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm, check_frozen=False):
    # replicator dynamics - one player is chosen at random and his strategy is copied with some p
    if not check_frozen:
        if len(neig_list) > 0:
            neig_id, neig_strategy, neig_payoff = neig_list[np.random.randint(len(neig_list))]
            probability = (neig_payoff - active_payoff) / (len(neig_list) * pay_off_norm)
        else:
            return active_strategy

        if probability > 0 and np.random.random() < probability:
            return neig_strategy
        else:
            return active_strategy
    else:
        for neig_id, neig_strategy, neig_payoff in neig_list:
            if neig_payoff > active_payoff and neig_strategy != active_strategy:
                return neig_strategy
        return active_strategy


def update_strategy(_type):
    if _type == const.UNCOND_IMITATION:
        return unconditional_imitation
    elif _type == const.REPLICATOR:
        return replicator_dynamics
    elif _type == const.BEST_RESPONSE:
        return best_response
    else:
        raise ValueError(f'Unknown type of the update strategy: {_type}')


###################################
#           main loops            #
###################################


def main_loop_async(graph, num_nodes, time_steps, update_func):
    last_update = None

    for time_step in range(time_steps):
        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy'][0]
        active_payoff = 0
        neig_list = []  # [(id, strategy, payoff), ...]

        # compute the payoff playing with neighbors
        for neig in neighbors:
            neig_list.append((neig, graph.vs(neig)['strategy'][0], graph.vs(neig)['last_payoff'][0]))
            active_payoff += graph['payoff_dict'][active_strategy][graph.vs(neig)['strategy'][0]]

        graph.vs(active_node)['last_payoff'] = active_payoff

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, graph['payoff_dict'], graph['payoff_norm'])
        graph.vs(active_node)['strategy'] = new_strategy

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


def compute_payoff(graph, node_index, payoff_dict):
    neighbors = graph.neighbors(node_index)
    node_strategy = graph.vs(node_index)['strategy'][0]
    payoff = 0

    # compute the payoff playing with neighbors
    for neig in neighbors:
        payoff += payoff_dict[node_strategy][graph.vs(neig)['strategy'][0]]

    return payoff


def main_loop_async_update_neigs(graph, num_nodes, time_steps, update_func):
    last_update = None

    for time_step in range(time_steps):
        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy'][0]
        active_payoff = 0
        neig_list = []  # [(id, strategy, payoff), ...]

        # compute the payoff playing with neighbors
        for neig in neighbors:
            neig_list.append((neig, graph.vs(neig)['strategy'][0], compute_payoff(graph, neig, graph['payoff_dict'])))
            active_payoff += graph['payoff_dict'][active_strategy][graph.vs(neig)['strategy'][0]]

        graph.vs(active_node)['last_payoff'] = active_payoff

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, graph['payoff_dict'], graph['payoff_norm'])
        graph.vs(active_node)['strategy'] = new_strategy

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


def main_loop_synchronous(graph, num_nodes, time_steps, update_func, no_update=False, only_payoff=False):
    last_update = None

    for time_step in range(time_steps):

        new_payoffs = []
        new_strategies = []

        # payoff loop
        for active_node in range(num_nodes):
            neighbors = graph.neighbors(active_node)
            active_strategy = graph.vs(active_node)['strategy'][0]
            active_payoff = 0

            # compute the payoff playing with neighbors
            for neig in neighbors:
                active_payoff += graph['payoff_dict'][active_strategy][graph.vs(neig)['strategy'][0]]

            new_payoffs.append(active_payoff)

        # strategy loop
        for active_node in range(num_nodes):
            neighbors = graph.neighbors(active_node)
            active_strategy = graph.vs(active_node)['strategy'][0]
            active_payoff = new_payoffs[active_node]

            neig_list = []  # [(id, strategy, payoff), ...]
            for neig in neighbors:
                neig_list.append((neig, graph.vs(neig)['strategy'][0], new_payoffs[neig]))

            # compute the new strategy
            new_strategy = update_func(active_payoff, active_strategy, neig_list, graph['payoff_dict'],
                                       graph['payoff_norm'], check_frozen=no_update)
            new_strategies.append(new_strategy)

            if new_strategy != active_strategy:
                last_update = time_step

        # update the whole network
        if not no_update:
            graph.vs()['last_payoff'] = new_payoffs
            if not only_payoff:
                graph.vs()['strategy'] = new_strategies

    return last_update


def initialize_payoff_multi(network, num_nodes):
    for active_node in range(num_nodes):
        if active_node in network.shared_nodes:
            layer_index = np.random.randint(0, network.num_layers)
            graph = network.get_layer(layer_index)

            active_payoff = compute_payoff(graph, active_node, graph['payoff_dict'])
            network.update_node(active_node, layer_index, trait_name='last_payoff', trait_value=active_payoff)

        elif active_node in network.individual_nodes:
            for i, graph in enumerate(network.layers):
                active_payoff = compute_payoff(graph, active_node, graph['payoff_dict'])
                network.update_node(active_node, i, trait_name='last_payoff', trait_value=active_payoff)

        else:
            raise AttributeError('This node is not shared nor individual! '
                                 'Something is seriously wrong with network generation...')
    return network


def main_loop_async_multi(network, num_nodes, time_steps, update_func):
    last_update = None

    for time_step in range(time_steps):
        layer_index = np.random.randint(0, network.num_layers)
        graph = network.get_layer(layer_index)

        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy'][0]
        active_payoff = 0
        neig_list = []  # [(id, strategy, payoff), ...]

        # compute the payoff playing with neighbors
        for neig in neighbors:
            neig_list.append((neig, graph.vs(neig)['strategy'][0], graph.vs(neig)['last_payoff'][0]))
            active_payoff += graph['payoff_dict'][active_strategy][graph.vs(neig)['strategy'][0]]

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, graph['payoff_dict'], graph['payoff_norm'])

        network.update_node(active_node, layer_index, trait_name='strategy', trait_value=new_strategy)
        network.update_node(active_node, layer_index, trait_name='last_payoff', trait_value=active_payoff)

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


def main_loop_async_multi_complete(network, num_nodes, time_steps, update_func):
    last_update = None

    for time_step in range(time_steps):
        layer_index = np.random.randint(0, network.num_layers)
        graph = network.get_layer(layer_index)

        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy'][0]
        active_payoff = 0
        neig_list = []  # [(id, strategy, payoff), ...]

        # compute the payoff playing with neighbors
        for neig in neighbors:
            neig_list.append((neig, graph.vs(neig)['strategy'][0], graph.vs(neig)['last_payoff'][0]))
            active_payoff += graph['payoff_dict'][active_strategy][graph.vs(neig)['strategy'][0]]

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, graph['payoff_dict'], graph['payoff_norm'])

        network.update_node(active_node, layer_index, trait_name='strategy', trait_value=new_strategy)
        network.update_node(active_node, layer_index, trait_name='last_payoff', trait_value=active_payoff)

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


####################################
#           simulations            #
####################################


def get_left_and_active(net, num_nodes, av_degree, multi=False):
    if multi:
        layers = net.layers
    else:
        layers = [net]

    left_num_res, active_res = [], []

    for g in layers:
        left_num = 0
        for node_id in range(num_nodes):
            if g.vs(node_id)['strategy'][0] == const.LEFT:
                left_num += 1
        left_num_res.append(left_num)

        if av_degree == num_nodes - 1:  # complete graph
            active = left_num * (num_nodes - left_num)
        else:
            active = 0
            for edge in g.get_edgelist():
                if g.vs(edge[0])['strategy'][0] != g.vs(edge[1])['strategy'][0]:
                    active += 1
        active_res.append(active)

    return (left_num_res, active_res) if len(layers) > 1 else (left_num_res[0], active_res[0])


def get_loop_function(loop_type, multi, num_nodes):
    if loop_type == const.ASYNC:
        if multi:
            main_loop = main_loop_async_multi
        else:
            main_loop = main_loop_async
        time_norm = num_nodes
    elif loop_type == const.SYNC:
        if multi:
            raise NotImplementedError('Synchronous update is not implemented for multilayer networks.')
        main_loop = main_loop_synchronous
        time_norm = 1.0
    else:
        raise ValueError(f'Unknown loop type: {loop_type}')

    return main_loop, time_norm


def run_trajectory(num_nodes=None, av_degree=None, loop_length=None, number_of_loops=None, loop_type=None,
                   payoff_type=None, update_str_type=None, b=None, R=None, P=None, T=None, S=None, check_frozen=False,
                   multi=False, multilayer=None, erdos=False, **kwargs):
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Running trajectory...')

    main_loop, time_norm = get_loop_function(loop_type, multi, num_nodes)
    update_func = update_strategy(update_str_type)

    if multi:
        if multilayer is None:
            raise ValueError('Configuration of layers is missing!')
        net = MultiNetCoordination(num_nodes=num_nodes, av_degree=av_degree, num_layers=multilayer['num_layers'],
                                   to_rewire=multilayer['to_rewire'], layers_config=multilayer['layers_config'],
                                   shared_nodes_ratio=multilayer['shared_nodes_ratio'], payoff_type=payoff_type,
                                   rewire_first_layer=multilayer['rewire_first_layer'])
        net = initialize_payoff_multi(net, num_nodes)

        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Rewired edges = {net.rewired_fraction}, '
              f'edge overlap = {net.compute_av_edge_overlap()}')
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Overlapping nodes = {len(net.shared_nodes)} '
              f'(of {net.num_nodes})')
    else:
        net = initialize_random_reg_net(num_nodes, av_degree, payoff_type=payoff_type, b=b, R=R, P=P, T=T, S=S,
                                        erdos=erdos)
        main_loop_synchronous(net, num_nodes, 1, update_func, only_payoff=True)

    left_num, active = get_left_and_active(net, num_nodes, av_degree, multi=multi)

    time_steps = [0]
    convergence_t = 0
    if multi:
        active_nums = [[2.0 * x / (av_degree * num_nodes) for x in active]]
        left_nums = [[x / num_nodes for x in left_num]]
    else:
        active_nums = [2.0 * active / (av_degree * num_nodes)]
        left_nums = [left_num / num_nodes]

    for i in range(number_of_loops):
        last_update_time = main_loop(net, num_nodes, loop_length, update_func)
        if last_update_time is not None:
            convergence_t = ((i * loop_length) + last_update_time) / time_norm

        left_num, active = get_left_and_active(net, num_nodes, av_degree, multi=multi)

        time_steps.append(((i + 1) * loop_length) / time_norm)  # MC time steps
        if multi:
            active_nums.append([2.0 * x / (av_degree * num_nodes) for x in active])
            left_nums.append([x / num_nodes for x in left_num])
        else:
            active_nums.append(2.0 * active / (av_degree * num_nodes))
            left_nums.append(left_num / num_nodes)

        if check_frozen:
            if multi:
                updated = None
                for g in net.layers:
                    last_update_time = main_loop_synchronous(g, num_nodes, 1, update_func, no_update=True)
                    if last_update_time == 0:
                        last_update_time = 1  # TODO check if works now
                    updated = updated or last_update_time
            else:
                updated = main_loop_synchronous(net, num_nodes, 1, update_func, no_update=True)
            if updated is None:
                break

    return convergence_t, time_steps, active_nums, left_nums


def get_stationary_state(num_nodes=None, av_degree=None, loop_length=None, number_of_loops=None, loop_type=None,
                         payoff_type=None, update_str_type=None, b=None, check_frozen=False, R=None, P=None, T=None,
                         S=None, erdos=False, **kwargs):
    g = initialize_random_reg_net(num_nodes, av_degree, payoff_type=payoff_type, b=b, R=R, P=P, T=T, S=S, erdos=erdos)
    update_func = update_strategy(update_str_type)
    main_loop_synchronous(g, num_nodes, 1, update_func, only_payoff=True)

    if loop_type == const.ASYNC:
        main_loop = main_loop_async
        time_norm = num_nodes
    elif loop_type == const.SYNC:
        main_loop = main_loop_synchronous
        time_norm = 1.0
    else:
        raise ValueError(f'Unknown loop type: {loop_type}')

    convergence_t = 0

    for i in range(number_of_loops):
        last_update_time = main_loop(g, num_nodes, loop_length, update_func)
        if last_update_time is not None:
            convergence_t = ((i * loop_length) + last_update_time) / time_norm

        if check_frozen:
            updated = main_loop_synchronous(g, num_nodes, 1, update_func, no_update=True)
            if updated is None:
                break

    left_num, active = get_left_and_active(g, num_nodes, av_degree)

    return convergence_t, left_num / num_nodes, 2.0 * active / (av_degree * num_nodes)


def get_stationary_state_multi(num_nodes=None, av_degree=None, loop_length=None, number_of_loops=None, loop_type=None,
                         payoff_type=None, update_str_type=None, check_frozen=False, multilayer=None, **kwargs):
    if multilayer is None:
        raise ValueError('Configuration of layers is missing!')

    net = MultiNetCoordination(num_nodes=num_nodes, av_degree=av_degree, num_layers=multilayer['num_layers'],
                               to_rewire=multilayer['to_rewire'], layers_config=multilayer['layers_config'],
                               shared_nodes_ratio=multilayer['shared_nodes_ratio'], payoff_type=payoff_type,
                               rewire_first_layer=multilayer['rewire_first_layer'])
    net = initialize_payoff_multi(net, num_nodes)

    main_loop, time_norm = get_loop_function(loop_type, True, num_nodes)
    update_func = update_strategy(update_str_type)

    convergence_t = 0

    for i in range(number_of_loops):
        last_update_time = main_loop(net, num_nodes, loop_length, update_func)
        if last_update_time is not None:
            convergence_t = ((i * loop_length) + last_update_time) / time_norm

        if check_frozen:
            updated = None
            for g in net.layers:
                last_update_time = main_loop_synchronous(g, num_nodes, 1, update_func, no_update=True)
                if last_update_time == 0:
                    last_update_time = 1
                updated = updated or last_update_time
            if updated is None:
                break

    left_num, active = get_left_and_active(net, num_nodes, av_degree, multi=True)
    active = [2.0 * x / (av_degree * num_nodes) for x in active]
    left_num = [x / num_nodes for x in left_num]

    return convergence_t, left_num, active


def get_stationary_state_sample(sample_size=None, multi=False, **kwargs):
    log.info(f'Running stationary sample...')

    if multi:
        get_function = get_stationary_state_multi
    else:
        get_function = get_stationary_state

    conv_time = []
    left_nums = []
    active_nums = []

    for i in range(sample_size):
        log.info(f'Running sample {i+1} of {sample_size}...')
        convergence_t, left_num, active = get_function(**kwargs)
        conv_time.append(convergence_t)
        left_nums.append(left_num)
        active_nums.append(active)
    return conv_time, left_nums, active_nums


##############################
#           tests            #
##############################


# if __name__ == '__main__':
#     N = 1000
#     k = 10
#     loop_steps = 100
#     g = initialize_random_reg_net(N, k)
#     ll = ig.Graph.layout(g)
#
#     active = 0
#     for edge in g.get_edgelist():
#         if g.vs(edge[0])['strategy'][0] != g.vs(edge[1])['strategy'][0]:
#             active += 1
#     left_num = 0
#     for node_id in range(N):
#         if g.vs(node_id)['strategy'][0] == const.LEFT:
#             left_num += 1
#
#     time_steps = [0]
#     active_nums = [2.0 * active / (k * N)]
#     left_nums = [left_num / N]
#     convergence_t = 0
#
#     payoff_dict, payoff_norm = payoff_matrix(const.COMPLEX, b=1)
#     update_func = update_strategy(const.UNCOND_IMITATION)
#     for i in range(100):
#         # for node_id in range(N):
#         #     if g.vs(node_id)['strategy'][0] == const.LEFT:
#         #         g.vs(node_id)['color'] = const.GREEN
#         #     else:
#         #         g.vs(node_id)['color'] = const.GOLD
#         # ig.plot(g, layout=ll)
#         last_update_time = main_loop_async(g, N, loop_steps, payoff_dict, payoff_norm, update_func)
#         if last_update_time is not None:
#             convergence_t = (i * loop_steps) + last_update_time
#
#         active = 0
#         for edge in g.get_edgelist():
#             if g.vs(edge[0])['strategy'][0] != g.vs(edge[1])['strategy'][0]:
#                 active += 1
#         left_num = 0
#         for node_id in range(N):
#             if g.vs(node_id)['strategy'][0] == const.LEFT:
#                 left_num += 1
#
#         time_steps.append((i+1)*loop_steps)
#         active_nums.append(2.0 * active / (k * N))
#         left_nums.append(left_num / N)
#
#     plt.plot(time_steps, left_nums, label='left frac')
#     plt.plot(time_steps, active_nums, label='active edges')
#     plt.axvline(convergence_t)
#     plt.legend()
#     plt.show()
#
