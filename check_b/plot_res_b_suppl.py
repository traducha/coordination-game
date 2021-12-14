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


def plot_res(str_type=const.UNCOND_IMITATION, av_degree=3, res_dir='imit_res_b_k3_new', out_dir='plots'):
    fig = plt.figure(figsize=(4, 3))
    plt.title('b', loc='left', fontweight='bold')
    plt.axvline(-2, linestyle='--', color='black', linewidth=0.9)

    # b_list = np.linspace(0.9, 2, 15)
    # b_list = np.linspace(0, 4, 30)
    # b_list = np.linspace(-9, 11, 100)
    b_list = np.linspace(-11, 11, 50)
    s_list = -b_list-1
    # b_list = np.linspace(-11, 30, 50)

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
                        num_nodes=1000, sample_size=20)
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
            plt.plot(-b-1, 1.0-value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[0])

    plt.plot(s_list, active, label=r'$\rho$', color=COLORS3[0], alpha=0.7)
    plt.plot(s_list, coop, label=r'$\alpha$', color=COLORS2[0])

    plt.legend()
    plt.xlabel(r'$S$')
    plt.xlim([-12, 10])
    plt.title(f"$k={av_degree}$")

    left, bottom, width, height = [0.7, 0.45, 0.2, 0.16]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    # ax2.axvline(max_b, linestyle='--', color='black')
    ax2.plot(b_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)
    # ax2.set_xlim([-13, 9])

    plt.tight_layout()

    plot_name = f"suppl_plots/suppl_b_{NAMES2[conf['update_str_type']]}_k{conf['av_degree']}_new.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


