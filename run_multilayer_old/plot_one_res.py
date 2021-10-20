# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import logging as log
import numpy as np
import json
import time
import os

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic
from config import config_values


COLORS = [const.GREEN, const.YELLOW]
COLORS2 = [const.GREEN_DARK, const.ORANGE]
COLORS3 = [const.REDISH, const.BLUE]

NAMES = {
    const.BEST_RESPONSE: 'Best response',
    const.UNCOND_IMITATION: 'Un. imitation',
    const.REPLICATOR: 'Replicator dyn.',
}

NAMES2 = {
    const.BEST_RESPONSE: 'best',
    const.UNCOND_IMITATION: 'ui',
    const.REPLICATOR: 'repl',
}


def plot_res(str_type=const.REPLICATOR, av_degree=8, res_dir='res_repl_b'):
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
        plt.plot(node_overlap_list, value, label=r'$\alpha$' + f'$_{i+1}$', color=COLORS2[i])
    plt.plot(node_overlap_list, [x[0]-x[1] for x in coop], label=r'$\Delta\alpha$', color='#777777', linestyle='--')

    # for i, value in enumerate(zip(*active)):
    #     plt.plot(node_overlap_list, value, label=f'L{i}' + r' $\rho$', color=COLORS3[i])


    plt.legend()
    plt.xlabel(r'$q$')
    # plt.title(f"{NAMES[conf['update_str_type']]}, N={conf['num_nodes']}, k={conf['av_degree']}")
              #+ (f", b={conf['b']}" if conf['b'] is not None else ''))

    # left, bottom, width, height = [0.57, 0.5, 0.15, 0.12]
    # ax2 = fig.add_axes([left, bottom, width, height])
    # ax2.patch.set_alpha(0.4)
    # ax2.plot(node_overlap_list, conv_time, color=const.BLUE, label=r'$\tau$', alpha=0.7)
    # # ax2.errorbar(node_overlap_list, conv_time_std, yerr=deviations[1], markerfacecolor='none', color=const.BLUE)
    # ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    # ax2.tick_params(axis='both', which='major', labelsize=8)

    description = ""
    for i, lc in enumerate(conf['multilayer']['layers_config']):
        description += f"layer {i+1} has $T_{i+1}={lc['T']}$, $S_{i+1}={lc['S']}$\n"
    plt.figtext(0.57, 0.3, description, fontsize=8)
    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.figtext(0.15, 0.8, 'd', fontsize=12, weight='bold')
    plt.tight_layout()

    plot_name = f"nov_{NAMES2[conf['update_str_type']]}_k{conf['av_degree']}.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res(str_type=const.REPLICATOR, av_degree=8, res_dir='res_repl_nov')


