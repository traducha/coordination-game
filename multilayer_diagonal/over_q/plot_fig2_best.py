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

    ###########################################
    T1_list = np.linspace(-1, -3, 21)[1:]
    S1 = None
    T2_list = -2.0 - T1_list
    S2 = None
    ###########################################

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    delta_s = []
    for T1, T2 in zip(T1_list, T2_list):
        T1 = round(T1, 2)
        T2 = round(T2, 2)
        dt = round(T2 - T1, 2)
        delta_s.append(dt)
        try:
            layers_config = config_values['multilayer']['layers_config']
            layers_config[0]['T'] = T1
            layers_config[0]['S'] = S1
            layers_config[1]['T'] = T2
            layers_config[1]['S'] = S2

            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=1.0, layers_config=layers_config)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k, sample_size=400)

            res_dir = f"res/long_res_{rules[update_str_type]}_k{k}_gap{dt}"
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception as e:
            conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k, sample_size=2001)
            res_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{dt}"
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
                    if dt > 2:
                        if random() < 0.05:
                            plt.plot(dt, value, marker='o', markerfacecolor='none', alpha=0.71, color=const.BROWN_LIGHT)
                    else:
                        if random() < 0.03:
                            plt.plot(dt, value, marker='o', markerfacecolor='none', alpha=1, color=const.BROWN_LIGHT)

    for i, value in enumerate(zip(*coop)):
        plt.plot(delta_s, value, color=const.BROWN)
        break



    # plt.text(0.78, 0.07, r"$\alpha_{q=1}= $ " + f"{round(coop[-1][0], 2)}", fontsize=9)

    # for i, value in enumerate(zip(*active)):
    #     plt.plot(delta_s, value, label=f'L{i}' + r' $\rho$', color=COLORS3[i], alpha=0.5)

    plt.xlabel(r'$\Delta S ( =\Delta T)$')
    plt.ylabel(r'$\alpha$')
    plt.title(f"{names[conf['update_str_type']]}")
    plt.title("b", loc='left', fontweight='bold')
    plt.xlim(left=0)
    plt.ylim([-0.04, 1.04])

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"plots/fig2_alpha_{res_dir[4:].split('gap')[0]}.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()
    return


if __name__ == '__main__':
    update_str_type = const.BEST_RESPONSE
    k = 8
    plot_res(str_type=update_str_type, av_degree=k)


