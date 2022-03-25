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


node_overlap_list = np.linspace(0, 1, 30)
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]


def plot_res(str_type=None, av_degree=None, res_dir=''):

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

    d_alpha = [x[0] - x[1] for x in coop]

    return d_alpha


if __name__ == '__main__':
    str_type = const.REPLICATOR
    k = 8

    colors = plt.cm.plasma(np.linspace(0, 1, 11))  # viridis

    fig = plt.figure(figsize=(4, 3))
    for i, gap in enumerate(ds_list):
        for directory in os.listdir(os.path.abspath('res')):
            directory = 'res/' + directory
            if os.path.isdir(directory) and f'res/res_{rules_dicts[str_type]}_k{k}' in directory:
                if f'_gap{gap}' in directory:
                    d_alpha = plot_res(str_type=str_type, av_degree=k, res_dir=directory)

                    plt.plot(node_overlap_list, d_alpha, label=f'{gap}', color=colors[i], linewidth=1.5, alpha=0.9)


    plt.xlabel(r'$q$')
    plt.ylabel(r'$\Delta \alpha$')
    plt.title(f'{names[str_type]}:' + r' $\Delta \alpha$ scaling')
    plt.legend(fontsize=8)

    plt.tight_layout()
    plot_name = f"plots/alhpa_sc_diag_{rules_dicts[str_type]}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

