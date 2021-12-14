# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os
import string

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


def plot_res(str_type=const.UNCOND_IMITATION):
    b_list = [x for x in np.linspace(-11, 11, 50) if x > 1]

    for aaa, b in enumerate(b_list):

        conv_time = []
        conv_time_std = []
        active = []
        active_std = []
        coop = []
        coop_std = []
        max_time = -float('inf')
        max_b = None

        fig = plt.figure(figsize=(4, 3))
        plt.title(string.ascii_lowercase[aaa], loc='left', fontweight='bold')
        s = round(-b-1, 2)

        for av_degree in range(2, 9):
            res_dir = f'imit_res_b_k{av_degree}_new'

            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, b=b, num_nodes=1000, sample_size=20)
            res, conf = read_stationary_generic(conf, directory=res_dir)

            time_mean = np.mean(res['convergence_time'])
            coop.append(1.0-np.mean(res['left_fraction']))
            coop_std.append(np.std(res['left_fraction']))
            active.append(np.mean(res['active_density']))
            active_std.append(np.std(res['active_density']))
            conv_time.append(time_mean)
            conv_time_std.append(np.std(res['convergence_time']))

            for i, value in enumerate(res['left_fraction']):
                plt.plot(av_degree, 1.0-value, marker='o', markerfacecolor='none', alpha=0.2, color=COLORS[0])

        plt.plot(range(2, 9), coop, label=r'$\alpha$', color=COLORS2[0])

        alpha = (-1 - s) / (1 - s)
        beta = - s / (1 - s)
        if alpha > beta:
            k_star = 1.0 / (1.0 - alpha)
        else:
            k_star = 2.0 / (2.0 - (alpha + beta))

        # plt.axvline(k_star, linestyle='--')

        # plt.legend()
        plt.xlabel(r'$k$')
        plt.ylabel(r'$\alpha$')
        plt.ylim([-0.05, 1.05])
        plt.title(f"$S={s}$")

        plt.tight_layout()

        plot_name = f"suppl_plots/suppl_k_{NAMES2[conf['update_str_type']]}_{string.ascii_lowercase[aaa]}.pdf"
        plt.savefig(plot_name)
        plt.show()
        plt.close()


if __name__ == '__main__':
    plot_res()


