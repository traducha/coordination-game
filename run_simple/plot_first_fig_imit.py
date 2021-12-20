# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import logging as log
import numpy as np
import json
import time
import os
from pprint import pprint
import random

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic
from config import config_values


def plot_res(str_type=const.UNCOND_IMITATION, N=1000, res_dir='res_imit_n1000'):
    fig = plt.figure(figsize=(4, 3))

    k_list = list(range(1, 61))

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    coop_up = []
    coop_down = []
    for k in k_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N, sample_size=500)
            res, conf = read_stationary_generic(conf, directory=res_dir)
        except Exception as e:
            print(k)
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet

        coop.append(np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

        array = np.array(res['left_fraction'])
        up = array[array > 0.5]
        down = array[array <= 0.5]
        if len(up) == 0:
            up = [0.5]
        coop_up.append(np.mean(up))
        coop_down.append(np.mean(down))

        for i, value in enumerate(res['left_fraction']):
            if random.random() < 0.2:
                plt.plot(k, value, marker='o', markerfacecolor='none', alpha=0.4, color=const.GREEN)

    ###############################################################################
    ###############################################################################

    er_coop_up = []
    er_coop_down = []
    for k in k_list:
        try:
            conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N, sample_size=500)
            res, conf = read_stationary_generic(conf, directory=res_dir + '_er')
        except Exception as e:
            print(k)
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet

        array = np.array(res['left_fraction'])
        up = array[array > 0.5]
        down = array[array <= 0.5]
        if len(up) == 0:
            up = [0.5]
        er_coop_up.append(np.mean(up))
        er_coop_down.append(np.mean(down))

    ###############################################################################
    ###############################################################################

    plt.plot(k_list, er_coop_up, linestyle='--', color='black', alpha=0.6)

    plt.plot(k_list, coop_up, color=const.ORANGE, label=r'$\alpha$')

    plt.plot(k_list, er_coop_down, linestyle='--', color='black', alpha=0.6, label=r'$\alpha_{ER}$')

    plt.plot(k_list, active, label=r'$\rho$', color=const.REDISH, alpha=0.8)

    plt.plot(k_list, coop_down, color=const.ORANGE)

    ###############################################################################
    ###############################################################################

    legend_elements = [
        Line2D([0], [0], marker='o', color=const.ORANGE, markerfacecolor='none', markeredgecolor=const.GREEN, lw=1.3,
               label=r'$\alpha$'),
        Line2D([0], [0], color='black', alpha=0.6, lw=1.3, linestyle='--', label=r'$\alpha_{ER}$'),
        Line2D([0], [0], color=const.REDISH, alpha=0.6, lw=1.3, label=r'$\rho$'),
                       ]
    plt.legend(loc=5, handles=legend_elements)
    plt.xlabel(r'$k$')
    # plt.ylabel(r'$\alpha$')
    plt.xlim([0, 60])
    plt.ylim([-0.03, 1.03])
    plt.title("c", loc='left', fontweight='bold')
    plt.title("UI")

    traj_files = {
        const.UNCOND_IMITATION: [
            'trajectory_n1000_k8_bNone_RNone_PNone_TNone_SNone_pay1_up2_loo5_len10_num50000_che1_sam500.json',
            'trajectory_n1000_k20_bNone_RNone_PNone_TNone_SNone_pay1_up2_loo5_len10_num50000_che1_sam500.json',
            'trajectory_n1000_k40_bNone_RNone_PNone_TNone_SNone_pay1_up2_loo5_len10_num50000_che1_sam500.json',
        ]
    }

    traj_coords = {
        const.UNCOND_IMITATION: [
            [14, 0.52],
            [10, 0.8],
            [3.5, 0.11],
        ]
    }

    # left, bottom, width, height = [0.4, 0.42, 0.3, 0.24]
    # ax2 = fig.add_axes([left, bottom, width, height])
    # ax2.patch.set_alpha(0.8)
    #
    # for i, traj_file in enumerate(traj_files[str_type]):
    #     with open(('trajectories/' + traj_file), 'r') as in_file:
    #         from_file = json.load(in_file)
    #     res, conf = from_file['results'], from_file['config']
    #     ax2.plot(res['time_steps'], res['left_fraction'], color=['#efc9af', '#104c91', '#1f8ac0'][i])
    #     ax2.text(traj_coords[str_type][i][0], traj_coords[str_type][i][1], f"$k$={conf['av_degree']}", fontsize=8)
    #
    # ax2.tick_params(axis='both', which='major', labelsize=8)
    # ax2.set_ylim([0, 1])
    # ax2.set_xlabel(r'$t$')
    # ax2.set_ylabel(r'$\alpha$')

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"simple_imit_traj.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


