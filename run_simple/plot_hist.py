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


def plot_res(str_type=const.REPLICATOR, N=1000, res_dir='res_repl_n1000'):
    fig = plt.figure(figsize=(5, 4.8))
    axs = fig.subplots(3, 3)
    # axs = list(axs[0]) + list(axs[1]) + list(axs[2])

    # RD and BR
    k_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # UI
    # k_list = [[2, 4, 5], [6, 8, 9], [10, 11, 15]]

    for i, ax_col in enumerate(axs):
        for j, ax in enumerate(ax_col):
            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k_list[i][j], num_nodes=N)
                res, conf = read_stationary_generic(conf, directory=res_dir)
            except Exception:
                print('ERROR? WHY?')  # it's if the simulation didn't finish yet

            ax.text(0.15, 0.8, f'k={k_list[i][j]}', transform=ax.transAxes)
            ax.hist(res['left_fraction'], bins=np.linspace(0.0, 1.0, 22), range=(0, 1), density=True, color='tomato', alpha=0.9)

            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k_list[i][j], num_nodes=N)
                res, conf = read_stationary_generic(conf, directory=res_dir+'_er')
            except Exception:
                print('ERROR? WHY?')  # it's if the simulation didn't finish yet

            ax.hist(res['left_fraction'], bins=np.linspace(0.0, 1.0, 22), range=(0, 1), density=True, color='cornflowerblue', alpha=0.7)

            ax.set_xlim([0, 1])
            ax.set_ylim([0, 12])
            if i == 0:
                if j == 0:
                    ax.set_ylim([0, 12])
                if j in [1, 2]:
                    ax.set_ylim([0, 12])
            # if i == 1:
            #     ax.set_ylim([0, 5])
            # if i == 2:
            #     if j == 2:
            #         ax.set_ylim([0, 5])
            if i == 2:
                ax.set_xlabel(r'$\alpha$')
            if j == 0:
                ax.set_ylabel(r'$P(\alpha)$')

    axs[0][1].set_title(f"{NAMES[conf['update_str_type']]}")
    axs[0][0].set_title(f"{NAMES15[conf['update_str_type']]}", loc='left', fontweight='bold')
    fig.tight_layout()
    plt.gcf().subplots_adjust(top=0.92, bottom=0.1, right=0.97, left=0.10)
    # fig.subplots_adjust(top=0.99)

    plot_name = f"simple_{NAMES2[conf['update_str_type']]}_N{conf['num_nodes']}_hist.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


