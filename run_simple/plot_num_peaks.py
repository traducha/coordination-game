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


def plot_res(str_type=const.UNCOND_IMITATION, N=1000, res_dir='res_imit_n1000_er'):
    fig = plt.figure(figsize=(4, 3))
    # axs = list(axs[0]) + list(axs[1]) + list(axs[2])

    # RD and BR
    k_list = list(range(1, 30))
    bins_num = 14

    for k in k_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet

        hist, bins = np.histogram(res['left_fraction'], bins=np.linspace(0.0, 1.0, bins_num))
        maxima = []
        for index in range(bins_num-1):
            if index == 0:
                if hist[index] > hist[index+1]:
                    maxima.append(bins[index])
            elif index == bins_num-2:
                if hist[index] > hist[index-1]:
                    maxima.append(bins[index+1])
            elif hist[index] > hist[index+1] and hist[index] > hist[index-1]:
                maxima.append(0.5*(bins[index]+bins[index+1]))
        for m in maxima:
            plt.scatter(k, m, color='black')

    plt.axhline(0.5, linestyle='--', color='black', alpha=0.5)
    plt.title(f"{NAMES[conf['update_str_type']]}")
    plt.title(f"{NAMES15[conf['update_str_type']]}", loc='left', fontweight='bold')
    fig.tight_layout()
    plt.gcf().subplots_adjust(top=0.92, bottom=0.1, right=0.97, left=0.10)
    # fig.subplots_adjust(top=0.99)

    plot_name = f"simple_{NAMES2[conf['update_str_type']]}_N{conf['num_nodes']}_maxima_er.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


