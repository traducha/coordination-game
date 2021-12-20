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

COLORS = [const.YELLOW, const.ORANGE, const.REDISH, const.GREEN_DARK, const.BLUE, const.VIOLET]


def plot_res(str_type=const.UNCOND_IMITATION, N=1000, res_dir='imit_res_n1000_b2'):
    fig = plt.figure(figsize=(4, 3))

    for iii, b in enumerate([5, 4, 3, 2, 1.5]):
        s = round(-b-1, 2)
        k_list = list(range(1, 201)) if b != 5 else list(range(1, 61))
        number_of_loops = 100 if b != 5 else 200
        sample_size = 100 if b != 5 else 500
        conv_time = []
        conv_time_std = []
        active = []
        active_std = []
        coop = []
        coop_std = []
        for k in k_list:
            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N, b=b,
                            number_of_loops=number_of_loops, sample_size=sample_size)
                res, conf = read_stationary_generic(conf, directory=f'imit_res_n1000_b{b}')
            except Exception:
                raise

            coop.append(1.0 - np.mean(res['left_fraction']))
            coop_std.append(np.std(res['left_fraction']))
            active.append(np.mean(res['active_density']))
            active_std.append(np.std(res['active_density']))
            conv_time.append(np.mean(res['convergence_time']))
            conv_time_std.append(np.std(res['convergence_time']))

        plt.plot(k_list, coop, color=COLORS[iii], label=f'$S = {s}$')

    plt.legend(fontsize=9)
    plt.xlabel(r'$k$')
    plt.ylabel(r'$\alpha$')
    plt.ylim([-0.03, 1.03])
    plt.xlim([0, 200])
    plt.title("b", loc='left', fontweight='bold')

    # left, bottom, width, height = [0.64, 0.6, 0.25, 0.2]
    # ax2 = fig.add_axes([left, bottom, width, height])
    # ax2.patch.set_alpha(0.4)
    # ax2.plot(k_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.8)
    # ax2.tick_params(axis='both', which='major', labelsize=8)
    #
    # ax2.set_xlabel(r'$k$')
    # ax2.set_ylabel(r'$\tau$')
    # ax2.set_xlim([0, 100])

    plt.tight_layout()
    plot_name = f"fig9b.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


