# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import logging as log
import numpy as np
import random
import json
import time
import os
from random import random

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic, rules_dicts as rules
from constants import rules_names as names
from config import config_values


COLORS = [const.GREEN, const.YELLOW]
COLORS2 = [const.GREEN_DARK, const.ORANGE]
COLORS3 = [const.REDISH, const.BLUE]


def func(x, a, b, c, d, e):
    return (a*(x**2.0) + b*x + e) / (1+np.exp(d*x + c))


def plot_res(str_type=None, av_degree=None):
    fig = plt.figure(figsize=(4, 3))

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    delta_s = []
    for T1 in np.linspace(0, 0.45, 20):
        T1 = round(T1, 3)
        S1 = -T1
        T2 = 1 - T1
        S2 = -T2
        ds = round(S1 - S2, 3)
        delta_s.append(ds)
        try:
            layers_config = config_values['multilayer']['layers_config']
            layers_config[0]['T'] = T1
            layers_config[0]['S'] = S1
            layers_config[1]['T'] = T2
            layers_config[1]['S'] = S2

            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=1.0, layers_config=layers_config)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k, sample_size=400)

            res_dir = f"res/long_res_{rules[update_str_type]}_k{k}_gap{ds}"
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception as e:
            conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k, sample_size=2001)
            res_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{ds}"
            res, conf = read_stationary_generic(conf, directory=res_dir)
            # print('ERROR? WHY?')  # it's if the simulation didn't finish yet

        coop.append([np.mean(value) for value in zip(*res['left_fraction'])])
        coop_std.append([np.std(value) for value in zip(*res['left_fraction'])])
        active.append([np.mean(value) for value in zip(*res['active_density'])])
        active_std.append([np.std(value) for value in zip(*res['active_density'])])
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        for j in range(conf['sample_size']):
            for i, value in enumerate(res['left_fraction'][j]):
                if random() < 0.03:
                    plt.plot(ds, value, marker='o', markerfacecolor='none', alpha=1, color=const.BROWN_LIGHT)
        if ds < 1:
            plt.plot(ds, 1, marker='o', markerfacecolor='none', alpha=1, color=const.BROWN_LIGHT)

    for i, value in enumerate(zip(*coop)):
        plt.plot(delta_s, value, color=const.BROWN)
        break

    plt.xlabel(r'$\Delta S ( =\Delta T)$')
    plt.ylabel(r'$\alpha$')
    plt.title(f"{names[conf['update_str_type']]}")
    plt.title("f", loc='left', fontweight='bold')
    plt.xlim(left=0)
    plt.ylim([-0.04, 1.04])

    plt.tight_layout()

    plot_name = f"plots/fig2_alpha_{res_dir[4:].split('gap')[0]}SH.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()
    return


if __name__ == '__main__':
    update_str_type = const.UNCOND_IMITATION
    k = 499
    plot_res(str_type=update_str_type, av_degree=k)


