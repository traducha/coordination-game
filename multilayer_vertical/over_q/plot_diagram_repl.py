# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import logging as log
import numpy as np
import json
import time
import os

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic, rules_dicts
from constants import rules_names as names
from config import config_values


COLORS = [const.GREEN, const.YELLOW]
COLORS2 = [const.GREEN_DARK, const.ORANGE]
COLORS3 = [const.REDISH, const.BLUE]
node_overlap_list = np.linspace(0, 1, 30)
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
q_c_list = [0.1724137931034483, 0.20689655172413793, 0.20689655172413793, 0.24137931034482757, 0.27586206896551724, 0.27586206896551724, 0.3448275862068966, 0.6551724137931034, 0.8620689655172413, 1.0]
q_c_fit_list = [0.14414414414414414, 0.1941941941941942, 0.1921921921921922, 0.22622622622622623, 0.23923923923923923, 0.25825825825825827, 0.3283283283283283, 0.3973973973973974, 0.5705705705705706, 0.8878878878878879]


def plot_res(str_type=None, av_degree=None, res_dir=''):
    fig = plt.figure(figsize=(4, 3))

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for nov in node_overlap_list:
        try:
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=0.0)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree)
            res, conf = read_stationary_generic(conf, directory=res_dir)

        coop.append([np.mean(value) for value in zip(*res['left_fraction'])])
        coop_std.append([np.std(value) for value in zip(*res['left_fraction'])])
        active.append([np.mean(value) for value in zip(*res['active_density'])])
        active_std.append([np.std(value) for value in zip(*res['active_density'])])
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

    l1_coop = None
    for i, value in enumerate(zip(*coop)):
        l1_coop = list(value)
        # break

    q_star = None
    for i, coop_value in enumerate(l1_coop):
        if coop_value >= 0.91:
            q_star = node_overlap_list[i]

    return l1_coop, q_star


if __name__ == '__main__':
    str_type = const.REPLICATOR
    k = 8

    diagram = []
    qs_list = []
    qs_ds_list = []
    for gap in ds_list:
        for directory in os.listdir(os.path.abspath('res')):
            directory = 'res/' + directory
            if os.path.isdir(directory) and f'res/res_{rules_dicts[str_type]}_k{k}' in directory:
                if f'_gap{gap}' in directory:
                    coop, qs = plot_res(str_type=str_type, av_degree=k, res_dir=directory)
                    diagram.append(coop)
                    if qs is not None:
                        qs_ds_list.append(gap)
                        qs_list.append(qs)

    for i in range(len(diagram)):
        for j in range(len(diagram[i])):
            if node_overlap_list[j] < q_c_fit_list[i]:
                diagram[i][j] = float('inf')

    plt.imshow(diagram, origin='lower', extent=[0, 1, 0.4, 4], aspect='auto', interpolation='none')  # hamming

    plt.plot(q_c_fit_list, ds_list, color='black')
    plt.plot(qs_list, qs_ds_list, color='black', linestyle='--')

    ax = plt.gca()
    ax.set_facecolor('thistle')  # plum
    plt.xlabel(r'$q$')
    plt.ylabel(r'$\Delta T$')
    cbar = plt.colorbar()
    cbar.mappable.set_clim(0, 1)
    plt.title(f'{names[str_type]}:' + r' $\langle \alpha \rangle$ for synchronized layers')

    plt.text(0.03, 3.6, 'no synchronization')
    plt.text(0.24, 2.8, 'Pareto-optimal', rotation=64, fontsize=8)
    plt.text(0.57, 1.2, '     coordination\non any strategy')

    plt.tight_layout()
    plot_name = f"plots/diagram_vert_{rules_dicts[str_type]}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

