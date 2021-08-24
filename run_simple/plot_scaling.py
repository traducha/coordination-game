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


COLORS = [const.ORANGE, const.GREEN_DARK, const.VIOLET]

NAMES = {
    const.BEST_RESPONSE: 'BR',
    const.UNCOND_IMITATION: 'UI',
    const.REPLICATOR: 'RD',
}

NAMES15 = {
    const.BEST_RESPONSE: 'b',
    const.UNCOND_IMITATION: 'c',
    const.REPLICATOR: 'a',
}

NAMES2 = {
    const.BEST_RESPONSE: 'best',
    const.UNCOND_IMITATION: 'ui',
    const.REPLICATOR: 'repl',
}


def plot_res(str_type=const.REPLICATOR, N_list=(1000, 2000, 4000),
             res_dir='res_repl_n'):

    fig = plt.figure(figsize=(4, 3))
    plt.axhline(0.5, linestyle='--', color='#bbbbbb')

    k_list = list(range(1, 61))
    max_time_list = []
    times = []

    for i, N in enumerate(N_list):
        conv_time = []
        coop_up = []
        coop_up_std = []
        coop_down = []
        max_time = float('-inf')
        k_c = None
        for k in k_list:
            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N)
                res, conf = read_stationary_generic(conf, directory=''.join([res_dir, str(N), '']))
            except Exception:
                print('ERROR? WHY?')  # it's if the simulation didn't finish yet

            array = np.array(res['left_fraction'])
            up = array[array > 0.5]
            down = array[array <= 0.5]
            if len(up) == 0:
                up = [0.5]
            coop_up.append(np.mean(up))
            coop_up_std.append(np.std(up))
            coop_down.append(np.mean(down))
            conv_time.append(np.mean(res['convergence_time']))

        plt.plot(k_list, coop_up, label=f'$N={N}$', color=COLORS[i])
        plt.plot(k_list, coop_down, color=COLORS[i])
        times.append(conv_time)

    plt.legend(loc=5, fontsize=7)
    plt.xlabel(r'$k$')
    plt.ylabel(r'$\alpha$')
    plt.title(f"{NAMES[conf['update_str_type']]}")
    plt.title(f"{NAMES15[conf['update_str_type']]}", loc='left', fontweight='bold')

    plt.xlim([0, 60])
    plt.ylim([0, 1])

    left, bottom, width, height = [0.38, 0.4, 0.3, 0.30]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.set_xlim([0, 30])
    # ax2.set_ylim([0, 50])
    ax2.set_xlabel(r'$k$')
    ax2.set_ylabel(r'$\tau$')
    for i, N in enumerate(N_list):
        ax2.plot(k_list, times[i], color=COLORS[i], alpha=0.7)

    plt.tight_layout()

    plot_name = f"simple_{NAMES2[conf['update_str_type']]}_scaling.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


