# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os
from pprint import pprint

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic
from config import config_values


COLORS = [const.GREEN, const.YELLOW]
COLORS2 = [const.GREEN_DARK, const.ORANGE]
COLORS3 = [const.REDISH, const.BLUE]

NAMES = {
    const.BEST_RESPONSE: 'Best response',
    const.UNCOND_IMITATION: 'Un. imitation',
    const.REPLICATOR: 'Replicator dyn.',
}

NAMES2 = {
    const.BEST_RESPONSE: 'best',
    const.UNCOND_IMITATION: 'ui',
    const.REPLICATOR: 'repl',
}


def plot_res(str_type=const.REPLICATOR, N=1000, res_dir='res_repl_n1000'):
    fig = plt.figure(figsize=(4, 3))

    k_list = list(range(1, 61))

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for k in k_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N, sample_size=500)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception as e:
            print(k)
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            # pprint(conf)
            # raise e

        coop.append(np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        for i, value in enumerate(res['left_fraction']):
            plt.plot(k, value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[0])
    plt.plot(100, 0, marker='o', markerfacecolor='none', alpha=1, color=COLORS[0], label=r'$\alpha$')

    # plt.plot(k_list, coop, label=r'$\alpha$', color=COLORS2[0])

    plt.plot(k_list, active, label=r'$\rho$', color=COLORS3[0])

    plt.legend(loc=5)
    plt.xlabel('k')
    plt.xlim([0, 60])
    plt.ylim([-0.03, 1.03])
    plt.title(f"{NAMES[conf['update_str_type']]}, N={conf['num_nodes']}")

    left, bottom, width, height = [0.75, 0.3, 0.15, 0.12]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(k_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"simple_{NAMES2[conf['update_str_type']]}_N{conf['num_nodes']}.png"
    # plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


