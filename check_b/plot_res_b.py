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
from config2 import config_values


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


def plot_res(str_type=const.UNCOND_IMITATION, av_degree=500, res_dir='res_b500_new_8000', out_dir='plots'):
    fig = plt.figure(figsize=(4, 3))
    plt.axvline(1, linestyle='--', color='black', linewidth=0.9)

    b_list = np.linspace(0.9, 2, 15)
    # b_list = np.linspace(0, 4, 30)
    # b_list = np.linspace(-9, 11, 100)

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    max_time = -float('inf')
    max_b = None
    for b in b_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, b=b,
                        num_nodes=8000, sample_size=50)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            # print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            # conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, b=0.6969696969696972)
            # res, conf = read_stationary_generic(conf, directory=res_dir)
            raise
        time_mean = np.mean(res['convergence_time'])

        coop.append(1.0-np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(time_mean)
        conv_time_std.append(np.std(res['convergence_time']))

        if time_mean > max_time and b < 1.4 and b > 1:
            max_time = time_mean
            max_b = b

        for i, value in enumerate(res['left_fraction']):
            plt.plot(b, 1.0-value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[0])

    plt.plot(b_list, coop, label=r'$\alpha$', color=COLORS2[0])

    plt.plot(b_list, active, label=r'$\rho$', color=COLORS3[0])

    plt.axvline(max_b, linestyle='--', color='black', linewidth=0.9)
    print(max_b)

    plt.gca().invert_xaxis()

    # plt.errorbar(averages[0], averages[3], yerr=deviations[3], markerfacecolor='none', color=const.REDISH)
    # plt.errorbar(averages[0], averages[2], yerr=deviations[2], markerfacecolor='none', color=const.GREEN_BRIGHT)

    plt.legend()
    plt.xlabel('b')
    plt.xlim([2, 0.9])
    plt.title(f"ER {NAMES[conf['update_str_type']]}, N={conf['num_nodes']}, k={conf['av_degree']}")
              #+ (f", b={conf['b']}" if conf['b'] is not None else ''))

    left, bottom, width, height = [0.75, 0.5, 0.15, 0.12]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.axvline(max_b, linestyle='--', color='black')
    ax2.plot(b_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.set_xlim([2, 1])

    plt.tight_layout()

    plot_name = f"er_ccg_b_{NAMES2[conf['update_str_type']]}_k{conf['av_degree']}_new.png"
    # plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


