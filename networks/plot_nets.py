# -*- coding: utf-8 -*-
from pprint import pprint
import sys
import igraph as ig
from matplotlib import pyplot as plt

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from networks import initialize_random_reg_net
import constants as const
from main import main_loop_async, main_loop_synchronous,\
    unconditional_imitation, replicator_dynamics, best_response

if __name__ == '__main__':
    n = 150
    update_func = unconditional_imitation

    for k in [3]:
        g = initialize_random_reg_net(n, k, erdos=False, payoff_type=const.SIMPLE)
        main_loop_synchronous(g, n, 1, update_func, only_payoff=True)

        # for node_idx in range(n):
        #     g.vs(node_idx)["label"] = g.vs(node_idx)['last_payoff']
        ll = ig.Graph.layout(g)
        # ig.plot(g, layout=ll)

        last_update = None
        while True:
            last_update = main_loop_async(g, n, n, update_func)
            print(last_update)
            last_update_time = main_loop_synchronous(g, n, 1, update_func, no_update=True)
            if last_update_time == 0:
                last_update_time = 1
            updated = None or last_update_time
            if updated is None:
                break

        g.vs()['size'] = 6
        print(len(g.components()))
        # print()

        for node_idx in range(n):
            if g.vs(node_idx)['strategy'][0] == const.RIGHT:
                g.vs(node_idx)['color'] = const.REDISH
            else:
                g.vs(node_idx)['color'] = const.BLUE
            # g.vs(node_idx)["label"] = g.vs(node_idx)['last_payoff']

        ig.plot(g, layout=ll, target=f'net_k{k}.pdf', bbox=[250, 250])



