# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D
import logging as log
import numpy as np
import json
import time
import os

import constants as const

import sys
import random
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

    coop = []
    coop2 = []
    for nov in node_overlap_list:
        try:
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree, sample_size=400)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet
            multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=0.0)
            conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree, sample_size=400)
            res, conf = read_stationary_generic(conf, directory=res_dir)

        coop.append([np.mean(value) for value in zip(*res['left_fraction'])])

        for j in range(conf['sample_size']):
            for i, value in enumerate(res['left_fraction'][j]):
                if random.random() < 0.05:
                    plt.plot(nov, value, marker='o', markerfacecolor='none', alpha=0.05, color=COLORS[i])

        multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov)
        conf = dict(config_values, multilayer=multi_conf, update_str_type=str_type, av_degree=av_degree, sample_size=100)
        res, conf = read_stationary_generic(conf, directory=res_dir.replace('long_', ''))
        coop2.append([np.mean(value) for value in zip(*res['left_fraction'])])

    for i, value in enumerate(zip(*(0.8*np.array(coop)+0.2*np.array(coop2)))):
        if i == 0:
            plt.plot(node_overlap_list, value, label=r'$\alpha^{I}$', color=COLORS[i])
        else:
            plt.plot(node_overlap_list, value, label=r'$\alpha^{II}$', color=COLORS[i], alpha=0.8)

    d_alpha = [x[0]-x[1] for x in coop]

    q_c = node_overlap_list[d_alpha.index(0.0)]
    plt.axvline(q_c, ymin=-0.5, ymax=0.03, color=const.REDISH)
    plt.text(q_c + 0.02, 0.04, r'$q_c \to 0$', fontsize=9)

    plt.axvline(0.758, ymin=1+0.5, ymax=1-0.03, color=const.RED)
    plt.text(0.758 + 0.06, 0.9, f'$q_p=0.76$', fontsize=9)

    plt.plot(node_overlap_list, d_alpha, label=r'$\Delta\alpha$', color='#21918c', linewidth=1)

    legend_elements = [
        Line2D([0], [0], marker='o', color=COLORS[0], markerfacecolor='none', markeredgecolor=COLORS[0], lw=1.3,
               label=r'$\alpha^{I}$'),
        Line2D([0], [0], marker='o', color=COLORS[1], markerfacecolor='none', markeredgecolor=COLORS[1], lw=1.3,
               label=r'$\alpha^{II}$', alpha=0.8),
        Line2D([0], [0], color='#21918c', alpha=1, lw=1.3, label=r'$\Delta\alpha$'),
                       ]
    plt.legend(loc='best', bbox_to_anchor=(0.65, 0.0, 0.25, 0.5), handles=legend_elements)
    plt.xlabel(r'$q$')
    ds = round(float(res_dir.split('gap')[1]), 1)
    plt.title(f"{names[conf['update_str_type']]}")
    plt.title(f"$\Delta S={ds}$", loc='right', fontsize=10)
    plt.title("f", loc='left', fontweight='bold')
    plt.ylim([-0.05, 1.05])


    description = ""
    def r(x):
        return round(x, 2)
    for i, lc in enumerate(conf['multilayer']['layers_config']):
        description += f"$T^I$=${r(lc['T'])}$\n$S^I$=${r(lc['S'])}$\n" if i == 0 else r"$T^{II}$="+f"${r(lc['T'])}$\n"+r"$S^{II}$="+f"${r(lc['S'])}$"
    plt.figtext(0.2, 0.45, description, fontsize=9)

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"plots/fig3_{res_dir[13:].split('gap')[0] + f'gap{ds}'}.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    str_type = const.UNCOND_IMITATION
    k = 499
    gap = 0.5


    for directory in os.listdir(os.path.abspath('res')):
        directory = 'res/' + directory
        if os.path.isdir(directory) and f'res/long_res_{rules_dicts[str_type]}_k{k}' in directory:
            if gap is None or f'_gap{gap}' == directory[-7:]:
                print(directory)
                plot_res(str_type=str_type, av_degree=k, res_dir=directory)

