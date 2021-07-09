# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os

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


def plot_res(str_type=const.UNCOND_IMITATION, av_degree=500, res_dir='res_S500_new', out_dir='plots'):
    fig = plt.figure(figsize=(4, 3))
    plt.axvline(-2, linestyle='--', color='black', linewidth=0.9)

    S_list = np.linspace(-12, 8, 100)

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for S in S_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=S, loop_type=const.ASYNC)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=-12.0, loop_type=const.ASYNC)
            res, conf = read_stationary_generic(conf, directory=res_dir)

        coop.append(np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        for i, value in enumerate(res['left_fraction']):
            plt.plot(S, value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[0])

    plt.plot(S_list, coop, label=r'$\alpha$', color=COLORS2[0])

    plt.plot(S_list, active, label=r'$\rho$', color=COLORS3[0])

    # plt.errorbar(averages[0], averages[3], yerr=deviations[3], markerfacecolor='none', color=const.REDISH)
    # plt.errorbar(averages[0], averages[2], yerr=deviations[2], markerfacecolor='none', color=const.GREEN_BRIGHT)

    plt.legend()
    plt.xlabel('S')
    plt.title(f"{NAMES[conf['update_str_type']]}, N={conf['num_nodes']}, k={conf['av_degree']}")
              #+ (f", b={conf['b']}" if conf['b'] is not None else ''))

    left, bottom, width, height = [0.75, 0.3, 0.15, 0.12]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(S_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    # ax2.errorbar(node_overlap_list, conv_time_std, yerr=deviations[1], markerfacecolor='none', color=const.BLUE)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)


    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"ccg_S_{NAMES2[conf['update_str_type']]}_k{conf['av_degree']}_new.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


