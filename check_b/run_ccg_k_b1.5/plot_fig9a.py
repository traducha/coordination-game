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


def plot_res(str_type=const.UNCOND_IMITATION, N=1000, res_dir='imit_res_n1000_b2'):
    fig = plt.figure(figsize=(4, 3))

    k_list = list(range(1, 101))

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for k in k_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N, b=2)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            raise

        coop.append(1.0 - np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        for i, value in enumerate(res['left_fraction']):
            if np.random.random() < 0.1:
                plt.plot(k, 1-value, marker='o', markerfacecolor='none', alpha=0.7, color=const.GREEN)

    plt.plot(k_list, coop, color=const.ORANGE, label=r'$\alpha$')

    plt.xlabel(r'$k$')
    plt.ylabel(r'$\alpha$')
    plt.ylim([-0.03, 1.03])
    plt.xlim([0, 100])
    plt.title("a", loc='left', fontweight='bold')

    left, bottom, width, height = [0.64, 0.6, 0.25, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(k_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    ax2.set_xlabel(r'$k$')
    ax2.set_ylabel(r'$\tau$')
    ax2.set_xlim([0, 100])

    plt.tight_layout()
    plot_name = f"fig9a.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


