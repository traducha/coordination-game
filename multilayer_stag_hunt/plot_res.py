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


def func(x, a, b, c, d, e):
    return (-(a*x)**2.0 + b*x + e) / (1+np.exp(d*x + c))


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
                plt.plot(nov, value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[i])

    for i, value in enumerate(zip(*coop)):
        plt.plot(node_overlap_list, value, label=f'L{i}' + r' $\alpha$', color=COLORS2[i])

    d_alpha = [x[0]-x[1] for x in coop]
    plt.plot(node_overlap_list, d_alpha, label=r'$\Delta\alpha$', color='black', linewidth=1, alpha=0.9)

    q_c = node_overlap_list[d_alpha.index(0.0)]
    plt.axvline(q_c, ymin=-0.5, ymax=0.03, color=const.REDISH)

    popt, pcov = curve_fit(func, node_overlap_list, d_alpha, p0=(10, 0, -1, 10, 1), maxfev=100000)
    plt.plot(np.linspace(0, 1, 100), func(np.linspace(0, 1, 100), *popt), color='#777777', linestyle='--')
    q_c_fit = next((x for x in np.linspace(0, 1, 1000) if func(x, *popt) < 0.01), None)
    plt.axvline(q_c_fit, ymin=-0.5, ymax=0.03, color=const.BLUE)

    plt.text(0.78, 0.07, r"$\alpha_{q=1}= $ " + f"{round(coop[-1][0], 2)}", fontsize=9)
    plt.text(-0.04, 0.52, f'$q_c=$ {round(q_c, 2)}', fontsize=9)
    plt.text(-0.04, 0.42, r'$q_c^{fit}=$ ' + f'{round(q_c_fit, 2)}', fontsize=9)

    for i, value in enumerate(zip(*active)):
        plt.plot(node_overlap_list, value, label=f'L{i}' + r' $\rho$', color=COLORS3[i], alpha=0.5)


    plt.legend(loc=5)
    plt.xlabel(r'$q$')
    ds = round(float(res_dir.split('gap')[1]), 1)
    plt.title(f"{names[conf['update_str_type']]}, N={conf['num_nodes']}, k={conf['av_degree']}, $\Delta$S={ds}")
    plt.ylim([-0.05, 1.05])

    left, bottom, width, height = [0.57, 0.5, 0.15, 0.12]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.4)
    ax2.plot(node_overlap_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    description = ""
    for i, lc in enumerate(conf['multilayer']['layers_config']):
        description += f"L{i} has R={lc['R']}, P={lc['P']}, T={round(lc['T'], 2)}, S={round(lc['S'], 2)}\n"
    plt.figtext(0.02, -0.03, description, fontsize=8)
    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"plots/{res_dir[8:].split('gap')[0] + f'gap{ds}'}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()

    return ds, q_c, q_c_fit


if __name__ == '__main__':
    str_type = const.BEST_RESPONSE
    k = 8

    ds_list = []
    q_c_list = []
    q_c_fit_list = []
    for directory in os.listdir(os.path.abspath('res')):
        directory = 'res/' + directory
        if os.path.isdir(directory) and f'res_{rules_dicts[str_type]}_k{k}' in directory:
            print(directory)
            ds, q_c, q_c_fit = plot_res(str_type=str_type, av_degree=k, res_dir=directory)
            ds_list.append(ds)
            q_c_list.append(q_c)
            q_c_fit_list.append(q_c_fit)

    print('ds_list =', ds_list)
    print('q_c_list =', q_c_list)
    print('q_c_fit_list =', q_c_fit_list)

