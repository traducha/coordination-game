# -*- coding: utf-8 -*-
import igraph as ig
import numpy as np

import constants as const
from networks import initialize_random_reg_net


#######################################
#           payoff updates            #
#######################################


def payoff_matrix(_type, b=None, R=None, P=None, T=None, S=None):
    # pay_off[mine][co-player]
    if _type == const.COMPLEX:
        if b is None:
            raise ValueError('The parameter b must be provided for the complex payoff matrix.')
        return {const.LEFT: {const.LEFT: 1, const.RIGHT: 0}, const.RIGHT: {const.LEFT: -b, const.RIGHT: 2}}, 2 + b
    elif _type == const.SIMPLE:
        return {const.LEFT: {const.LEFT: 1, const.RIGHT: 0}, const.RIGHT: {const.LEFT: 0, const.RIGHT: 1}}, 1
    elif _type == const.GENERIC:
        if R is None or P is None or T is None or S is None:
            raise ValueError('The parameters R, P, T, and S must be provided for the generic payoff matrix.')
        return {const.LEFT: {const.LEFT: R, const.RIGHT: S}, const.RIGHT: {const.LEFT: T, const.RIGHT: P}},\
               max([R, P, T, S]) - min([R, P, T, S])
    else:
        raise ValueError(f'Unrecognized matrix type: {_type}')


def unconditional_imitation(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm, **kwargs):
    # unconditional imitation - copy the most succesful neig if he's better
    max_neig_payoff = -10000
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
        neig_id, neig_strategy, neig_payoff = neig_list[np.random.randint(len(neig_list))]
        probability = (neig_payoff - active_payoff) / (len(neig_list) * pay_off_norm)

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


def main_loop_async_old(graph, num_nodes, time_steps, pay_off_dict, pay_off_norm, update_func):
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
            active_payoff += pay_off_dict[active_strategy][graph.vs(neig)['strategy'][0]]

        graph.vs(active_node)['last_payoff'] = active_payoff

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm)
        graph.vs(active_node)['strategy'] = new_strategy

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


def compute_payoff(graph, node_index, pay_off_dict):
    neighbors = graph.neighbors(node_index)
    node_strategy = graph.vs(node_index)['strategy'][0]
    payoff = 0

    # compute the payoff playing with neighbors
    for neig in neighbors:
        payoff += pay_off_dict[node_strategy][graph.vs(neig)['strategy'][0]]

    return payoff


def main_loop_async(graph, num_nodes, time_steps, pay_off_dict, pay_off_norm, update_func):
    last_update = None

    for time_step in range(time_steps):
        active_node = np.random.randint(0, num_nodes)
        neighbors = graph.neighbors(active_node)

        active_strategy = graph.vs(active_node)['strategy'][0]
        active_payoff = 0
        neig_list = []  # [(id, strategy, payoff), ...]

        # compute the payoff playing with neighbors
        for neig in neighbors:
            neig_list.append((neig, graph.vs(neig)['strategy'][0], compute_payoff(graph, neig, pay_off_dict)))
            active_payoff += pay_off_dict[active_strategy][graph.vs(neig)['strategy'][0]]

        graph.vs(active_node)['last_payoff'] = active_payoff

        # update the strategy
        new_strategy = update_func(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm)
        graph.vs(active_node)['strategy'] = new_strategy

        if new_strategy != active_strategy:
            last_update = time_step

    return last_update


def main_loop_synchronous(graph, num_nodes, time_steps, pay_off_dict, pay_off_norm, update_func, no_update=False):
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
                active_payoff += pay_off_dict[active_strategy][graph.vs(neig)['strategy'][0]]

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
            new_strategy = update_func(active_payoff, active_strategy, neig_list, pay_off_dict, pay_off_norm,
                                       check_frozen=no_update)
            new_strategies.append(new_strategy)

            if new_strategy != active_strategy:
                last_update = time_step

        # update the whole network
        if not no_update:
            graph.vs()['strategy'] = new_strategies
            graph.vs()['last_payoff'] = new_payoffs

    return last_update


####################################
#           simulations            #
####################################


def get_left_and_active(g, num_nodes):
    active = 0
    for edge in g.get_edgelist():
        if g.vs(edge[0])['strategy'][0] != g.vs(edge[1])['strategy'][0]:
            active += 1
    left_num = 0
    for node_id in range(num_nodes):
        if g.vs(node_id)['strategy'][0] == const.LEFT:
            left_num += 1
    return left_num, active


def run_trajectory(num_nodes=None, av_degree=None, loop_length=None, number_of_loops=None, loop_type=None,
                   payoff_type=None, update_str_type=None, b=None, check_frozen=False, **kwargs):
    print('Running trajectory...')
    g = initialize_random_reg_net(num_nodes, av_degree)
    payoff_dict, payoff_norm = payoff_matrix(payoff_type, b=b)
    update_func = update_strategy(update_str_type)

    if loop_type == const.ASYNC:
        main_loop = main_loop_async_old  # TODO
        time_norm = num_nodes
    elif loop_type == const.SYNC:
        main_loop = main_loop_synchronous
        time_norm = 1.0
    else:
        raise ValueError(f'Unknown loop type: {loop_type}')

    left_num, active = get_left_and_active(g, num_nodes)

    time_steps = [0]
    active_nums = [2.0 * active / (av_degree * num_nodes)]
    left_nums = [left_num / num_nodes]
    convergence_t = 0

    for i in range(number_of_loops):
        last_update_time = main_loop(g, num_nodes, loop_length, payoff_dict, payoff_norm, update_func)
        if last_update_time is not None:
            convergence_t = ((i * loop_length) + last_update_time) / time_norm

        left_num, active = get_left_and_active(g, num_nodes)

        time_steps.append(((i + 1) * loop_length) / time_norm)  # MC time steps
        active_nums.append(2.0 * active / (av_degree * num_nodes))
        left_nums.append(left_num / num_nodes)

        if check_frozen:
            updated = main_loop_synchronous(g, num_nodes, 1, payoff_dict, payoff_norm, update_func,
                                            no_update=True)
            if updated is None:
                break

    return convergence_t, time_steps, active_nums, left_nums


def get_stationary_state(num_nodes=None, av_degree=None, loop_length=None, number_of_loops=None, loop_type=None,
                         payoff_type=None, update_str_type=None, b=None, check_frozen=False, R=None, P=None, T=None,
                         S=None, **kwargs):
    g = initialize_random_reg_net(num_nodes, av_degree)
    payoff_dict, payoff_norm = payoff_matrix(payoff_type, b=b, R=R, P=P, T=T, S=S)
    update_func = update_strategy(update_str_type)

    if loop_type == const.ASYNC:
        main_loop = main_loop_async_old  # TODO
        time_norm = num_nodes
    elif loop_type == const.SYNC:
        main_loop = main_loop_synchronous
        time_norm = 1.0
    else:
        raise ValueError(f'Unknown loop type: {loop_type}')

    convergence_t = 0

    for i in range(number_of_loops):
        last_update_time = main_loop(g, num_nodes, loop_length, payoff_dict, payoff_norm, update_func)
        if last_update_time is not None:
            convergence_t = ((i * loop_length) + last_update_time) / time_norm

        if check_frozen:
            updated = main_loop_synchronous(g, num_nodes, 1, payoff_dict, payoff_norm, update_func,
                                            no_update=True)
            if updated is None:
                break

    left_num, active = get_left_and_active(g, num_nodes)

    return convergence_t, left_num / num_nodes, 2.0 * active / (av_degree * num_nodes)


def get_stationary_state_sample(sample_size=None, **kwargs):
    print('Running stationary sample...')
    conv_time = []
    left_nums = []
    active_nums = []
    for i in range(sample_size):
        convergence_t, left_num, active = get_stationary_state(**kwargs)
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
