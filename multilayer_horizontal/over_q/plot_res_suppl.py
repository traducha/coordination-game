# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
import logging as log
import numpy as np
import json
import time
import os
import random

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic, rules_dicts
from constants import rules_names as names
from config import config_values


COLORS = ['#fde725', '#440154']


def func(x, a, b, c, d, e):
    return (a*(x**2.0) + b*x + e) / (1+np.exp(d*x + c))


def plot_res(str_type=None, av_degree=None, res_dir=''):
    fig = plt.figure(figsize=(4, 3))

    node_overlap_list = np.linspace(0, 1, 30)

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

        for j in range(conf['sample_size']):
            for i, value in enumerate(res['left_fraction'][j]):
                if random.random() < 0.2:
                    plt.plot(nov, value, marker='o', markerfacecolor='none', alpha=0.1, color=COLORS[i])

    for i, value in enumerate(zip(*coop)):
        if i == 0:
            plt.plot(node_overlap_list, value, label=r'$\alpha^{I}$', color=COLORS[i])
        else:
            plt.plot(node_overlap_list, value, label=r'$\alpha^{II}$', color=COLORS[i], alpha=0.8)

    d_alpha = [x[0]-x[1] for x in coop]
    plt.plot(node_overlap_list, d_alpha, label=r'$\Delta\alpha$', color='#21918c', linewidth=1, alpha=0.9)

    q_c = node_overlap_list[d_alpha.index(0.0)]
    plt.axvline(q_c, ymin=-0.5, ymax=0.03, color=const.REDISH)

    # fitting
    popt, pcov = curve_fit(func, node_overlap_list, d_alpha, p0=(-10, 0, -1, 10, 1), maxfev=10000)
    print(popt)
    plt.plot(np.linspace(0, 1, 100), func(np.linspace(0, 1, 100), *popt), color='#777777', linestyle='--')
    q_c_fit = next((x for x in np.linspace(0, 1, 1000) if func(x, *popt) < 0.01), 1.0)
    plt.axvline(q_c_fit, ymin=-0.01, ymax=0.03, color=const.BLUE)

    # plt.text(0.78, 0.07, r"$\alpha_{q=1}= $ " + f"{round(coop[-1][0], 2)}", fontsize=9)
    if str_type == const.REPLICATOR:
        plt.text(q_c + 0.025, 0.15, f'$q_c=$ {round(q_c, 2)}', fontsize=9)
        plt.text(q_c + 0.025, 0.05, r'$q_c^{fit}=$ ' + f'{round(q_c_fit, 2)}', fontsize=9)
    elif str_type == const.BEST_RESPONSE:
        plt.text(0.55, 0.15, f'$q_c=$ {round(q_c, 2)}', fontsize=9)
        plt.text(0.55, 0.05, r'$q_c^{fit}=$ ' + f'{round(q_c_fit, 2)}', fontsize=9)

    legend_elements = [
        Line2D([0], [0], marker='o', color=COLORS[0], markerfacecolor='none', markeredgecolor=COLORS[0], lw=1.3,
               label=r'$\alpha^{I}$'),
        Line2D([0], [0], marker='o', color=COLORS[1], markerfacecolor='none', markeredgecolor=COLORS[1], lw=1.3,
               label=r'$\alpha^{II}$', alpha=0.8),
        Line2D([0], [0], color='#21918c', alpha=1, lw=1.3, label=r'$\Delta\alpha$'),
    ]
    plt.legend(loc='best', bbox_to_anchor=(0.5, 0.5, 0.5, 0.5), handles=legend_elements)
    plt.xlabel(r'$q$')
    ds = round(float(res_dir.split('gap')[1]), 1)
    plt.title(f"{names[conf['update_str_type']]}, $N$={conf['num_nodes']}, $k$={conf['av_degree']}, $\Delta S$={ds}")
    plt.ylim([-0.05, 1.05])

    description = ""
    for i, lc in enumerate(conf['multilayer']['layers_config']):
        description += f"$T^I$=${round(lc['T'], 2)}$\n$S^I$=${round(lc['S'], 2)}$\n" if i == 0 else r"$T^{II}$=" + f"${round(lc['T'], 2)}$\n" + r"$S^{II}$=" + f"${round(lc['S'], 2)}$"
    plt.figtext(0.13, 0.42, description, fontsize=9)
    plt.tight_layout()

    plot_name = f"plots/{res_dir[8:].split('gap')[0] + f'gap{ds}'}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

    print("(ds, q_c, q_c_fit) = ", ds, q_c, q_c_fit)
    return ds, q_c, q_c_fit


if __name__ == '__main__':
    str_type = const.BEST_RESPONSE
    k = 8
    gap = None

    ds_list = []
    q_c_list = []
    q_c_fit_list = []
    for directory in os.listdir(os.path.abspath('res')):
        directory = 'res/' + directory
        if os.path.isdir(directory) and f'res/res_{rules_dicts[str_type]}_k{k}' in directory:
            if gap is None or f'_gap{gap}' in directory:
                print(directory)
                ds, q_c, q_c_fit = plot_res(str_type=str_type, av_degree=k, res_dir=directory)
                ds_list.append(ds)
                q_c_list.append(q_c)
                q_c_fit_list.append(q_c_fit)

    print('ds_list =', ds_list)
    print('q_c_list =', q_c_list)
    print('q_c_fit_list =', q_c_fit_list)

