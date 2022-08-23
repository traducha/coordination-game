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
    for ww, nov in enumerate(node_overlap_list):
        try:
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=node_overlap_list[ww-1])
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

    # for i, value in enumerate(zip(*active)):
    #     plt.plot(node_overlap_list, value, label=f'L{i}' + r' $\rho$', color=COLORS3[i], alpha=0.5)

    legend_elements = [
        Line2D([0], [0], marker='o', color=COLORS[0], markerfacecolor='none', markeredgecolor=COLORS[0], lw=1.3,
               label=r'$\alpha^{I}$'),
        Line2D([0], [0], marker='o', color=COLORS[1], markerfacecolor='none', markeredgecolor=COLORS[1], lw=1.3,
               label=r'$\alpha^{II}$', alpha=0.8),
        Line2D([0], [0], color='#21918c', alpha=1, lw=1.3, label=r'$\Delta\alpha$'),
    ]
    plt.legend(loc='best', bbox_to_anchor=(0.5, 0.0, 0.5, 0.5), handles=legend_elements)
    plt.xlabel(r'$q$')
    ds = round(float(res_dir.split('gap')[1]), 1)
    plt.title(f"{names[conf['update_str_type']]}, $N$={conf['num_nodes']}, $k$={conf['av_degree']}, $\Delta S$={ds}")
    plt.ylim([-0.05, 1.05])

    # left, bottom, width, height = [0.57, 0.5, 0.15, 0.12]
    # ax2 = fig.add_axes([left, bottom, width, height])
    # ax2.patch.set_alpha(0.4)
    # ax2.plot(node_overlap_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    # ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    # ax2.tick_params(axis='both', which='major', labelsize=8)

    description = ""
    for i, lc in enumerate(conf['multilayer']['layers_config']):
        description += f"$T^I$=${lc['T']}$\n$S^I$=${lc['S']}$\n" if i == 0 else r"$T^{II}$=" + f"${lc['T']}$\n" + r"$S^{II}$=" + f"${lc['S']}$"
    plt.figtext(0.25, 0.25, description, fontsize=9)
    plt.tight_layout()

    plot_name = f"plots/{res_dir[8:].split('gap')[0] + f'gap{ds}'}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

    print("(ds, q_c, q_c_fit) = ", ds, q_c, None)
    return ds, q_c, None


if __name__ == '__main__':
    str_type = const.UNCOND_IMITATION
    k = 499
    gap = None

    ds_list = []
    q_c_list = []
    q_c_fit_list = []
    for directory in os.listdir(os.path.abspath('res')):
        directory = 'res/' + directory
        if os.path.isdir(directory) and f'res/res_{rules_dicts[str_type]}_k{k}' in directory:
            if gap is None or f'_gap{gap}' in directory:
                print(directory)

                g = float(directory[-3:])
                if int(g*10) % 4 != 0:
                    continue

                ds, q_c, q_c_fit = plot_res(str_type=str_type, av_degree=k, res_dir=directory)
                ds_list.append(ds)
                q_c_list.append(q_c)
                q_c_fit_list.append(q_c_fit)

    print('ds_list =', ds_list)
    print('q_c_list =', q_c_list)
    print('q_c_fit_list =', q_c_fit_list)

