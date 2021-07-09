# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import logging as log
import numpy as np
import random
import json

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic
from config2 import config_values


def plot_res(str_type=const.UNCOND_IMITATION, av_degree=8, res_dir='res_b8_new'):
    fig = plt.figure(figsize=(4, 3.2))
    ax1 = fig.add_subplot(111)
    ax1.set_xticks([-10, -5, 0, 5])
    plt.axvline(-2, linestyle='--', color='black', linewidth=0.9)

    b_list = np.linspace(-9, 11, 100)
    s_list = [-x-1.0 for x in b_list]

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for b in b_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, b=b,
                        num_nodes=1000, sample_size=100)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception:
            raise
        time_mean = np.mean(res['convergence_time'])

        coop.append(1.0-np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(time_mean)
        conv_time_std.append(np.std(res['convergence_time']))

        for i, value in enumerate(res['left_fraction']):
            if random.random() < 0.1:
                plt.plot(-b-1, 1.0-value, marker='o', markerfacecolor='none', alpha=0.4, color=const.GREEN)

    er_active = []
    er_coop = []
    for b in b_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, b=b,
                        num_nodes=1000, sample_size=100)
            res, conf = read_stationary_generic(conf, directory='imit_res_b_k8_new_er')
        except Exception:
            raise
        er_coop.append(1.0 - np.mean(res['left_fraction']))
        er_active.append(np.mean(res['active_density']))

    ################################################################################
    ################################################################################

    plt.plot(s_list, active, label=r'$\rho$', color=const.REDISH, alpha=0.8)

    plt.plot(s_list, er_coop, linestyle='--', color='black', alpha=0.6)

    plt.plot(s_list, coop, color=const.ORANGE, label=r'$\alpha$')

    legend_elements = [
        Line2D([0], [0], marker='o', color=const.ORANGE, markerfacecolor='none', markeredgecolor=const.GREEN, lw=1.3,
               label=r'$\alpha$'),
        Line2D([0], [0], color='black', alpha=0.6, lw=1.3, linestyle='--', label=r'$\alpha_{ER}$'),
        Line2D([0], [0], color=const.REDISH, alpha=0.6, lw=1.3, label=r'$\rho$'),
    ]
    plt.legend(loc=2, handles=legend_elements)
    plt.xlabel(r'$S$')
    plt.xlim([-12, 8])
    plt.ylim([-0.05, 1.05])
    plt.title('a', loc='left', fontweight='bold')

    _ax1 = ax1.twiny()
    _ax1.set_xlim(ax1.get_xlim())
    new_ticks = [-11, -6, -1, 4]
    _ax1.set_xticks(new_ticks)
    _ax1.set_xticklabels([-x-1 for x in new_ticks])
    _ax1.set_xlabel(r'$b$')

    #####################################################################
    #####################################################################

    traj_files = {
        const.UNCOND_IMITATION: [
            'trajectory_n1000_k8_bNone_R1_P0_T-1_S0_pay1000_up2_loo5_len10_num50000_che1_sam100.json',
            'trajectory_n1000_k8_bNone_R1_P0_T-1_S-5_pay1000_up2_loo5_len10_num50000_che1_sam100.json',
            'trajectory_n1000_k8_bNone_R1_P0_T-1_S-10_pay1000_up2_loo5_len10_num50000_che1_sam100.json',
        ]
    }

    traj_coords = {
        const.UNCOND_IMITATION: [
            [3, 0.8],
            [4, 0.21],
            [-0.35, 0.04],
        ]
    }

    left, bottom, width, height = [0.665, 0.37, 0.29, 0.25]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.8)

    for i, traj_file in enumerate(traj_files[str_type]):
        with open(('trajectories_/' + traj_file), 'r') as in_file:
            from_file = json.load(in_file)
        res, conf = from_file['results'], from_file['config']
        ax2.plot(res['time_steps'], res['left_fraction'], color=['#104c91', '#efc9af', '#1f8ac0'][i])
        ax2.text(traj_coords[str_type][i][0], traj_coords[str_type][i][1], f"$S$={conf['S']}", fontsize=8)

    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.set_ylim([0, 1])
    ax2.set_xlabel(r'$\tau$')
    ax2.set_ylabel(r'$\alpha$')

    plt.tight_layout()

    plot_name = f"imit_S_b_a.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


