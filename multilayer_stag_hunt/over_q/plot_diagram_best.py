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
ds_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
q_c_list = [0.5517241379310345, 0.5517241379310345, 0.8620689655172413, 0.8620689655172413, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
q_c_fit_list = [0.5705705705705706, 0.5445445445445445, 0.8418418418418419, 0.8318318318318318, 0.9879879879879879, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999]


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
        if coop_value >= 0.94:
            q_star = node_overlap_list[i]

    return l1_coop, q_star


if __name__ == '__main__':
    str_type = const.BEST_RESPONSE
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
            if node_overlap_list[j] < q_c_list[i]:
                diagram[i][j] = float('inf')

    plt.imshow(diagram, origin='lower', extent=[0, 1, 0.1, 1], aspect='auto', interpolation='none')  # hamming

    cut = 5
    plt.plot(q_c_list[:cut], ds_list[:cut], color='black')
    plt.plot(q_c_fit_list[cut-1:], ds_list[cut-1:], color='black', linestyle='-.')

    ax = plt.gca()
    ax.set_facecolor('plum')  # plum
    plt.xlabel(r'$q$')
    plt.ylabel(r'$\Delta S (= \Delta T)$')
    cbar = plt.colorbar()
    cbar.mappable.set_clim(0, 1)
    plt.title(f'{names[str_type]}:' + r' $\langle \alpha \rangle$ for synchronized layers')

    plt.text(0.1, 2.5/4, 'no synchronization')
    plt.text(0.89, 3.65/4, 'synchronized layers,\nbut no coordination', rotation=90, fontsize=8)
    plt.text(0.58, 0.5/4, '     coordination\non any strategy')

    plt.tight_layout()
    plot_name = f"plots/diagram_stag_{rules_dicts[str_type]}_k{k}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

