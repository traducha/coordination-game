# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import logging as log
import numpy as np
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
    # T1 = -1
    # S1_list = np.linspace(-1.95, 0, 40)
    # T2 = -1
    # S2_list = np.linspace(-2.05, -4, 40)
    ###########################################

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    delta_s = []
    for T1 in np.linspace(0, 0.45, 10):
        T1 = round(T1, 2)
        S1 = -T1
        T2 = 1 - T1
        S2 = -T2
        ds = round(S1 - S2, 2)
        delta_s.append(ds)
        try:
            layers_config = config_values['multilayer']['layers_config']
            layers_config[0]['T'] = T1
            layers_config[0]['S'] = S1
            layers_config[1]['T'] = T2
            layers_config[1]['S'] = S2

            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=1.0, layers_config=layers_config)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k)

            res_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{ds}"
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception as e:
            res_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{ds}"
            res, conf = read_stationary_generic(conf, directory=res_dir)
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet


        coop.append([np.mean(value) for value in zip(*res['left_fraction'])])
        coop_std.append([np.std(value) for value in zip(*res['left_fraction'])])
        active.append([np.mean(value) for value in zip(*res['active_density'])])
        active_std.append([np.std(value) for value in zip(*res['active_density'])])
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        for j in range(conf['sample_size']):
            for i, value in enumerate(res['left_fraction'][j]):
                if random() < 1:
                    plt.plot(ds, value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[i])

    for i, value in enumerate(zip(*coop)):
        plt.plot(delta_s, value, color=COLORS2[i])
        break



    # plt.text(0.78, 0.07, r"$\alpha_{q=1}= $ " + f"{round(coop[-1][0], 2)}", fontsize=9)

    # for i, value in enumerate(zip(*active)):
    #     plt.plot(delta_s, value, label=f'L{i}' + r' $\rho$', color=COLORS3[i], alpha=0.5)

    plt.xlabel(r'$\Delta S (= \Delta T)$')
    plt.ylabel(r'$\alpha$')
    plt.title(f"{names[conf['update_str_type']]}, N={conf['num_nodes']}, k={conf['av_degree']}, q=1")
    plt.ylim([-0.04, 1.04])

    left, bottom, width, height = [0.7, 0.32, 0.15, 0.12]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(delta_s, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"plots/alpha_{res_dir[4:].split('gap')[0]}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()
    return


if __name__ == '__main__':
    update_str_type = const.UNCOND_IMITATION
    k = 499
    plot_res(str_type=update_str_type, av_degree=k)


