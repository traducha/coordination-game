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


COLORS = [const.ORANGE, const.REDISH, const.GREEN_DARK, const.BLUE][::-1]

NAMES = {
    const.BEST_RESPONSE: 'BR',
    const.UNCOND_IMITATION: 'UI',
    const.REPLICATOR: 'RD',
}

NAMES2 = {
    const.BEST_RESPONSE: 'best',
    const.UNCOND_IMITATION: 'imit',
    const.REPLICATOR: 'repl',
}


def plot_res(str_type=None, av_degree=None, T=None, res_dir=None,
             color=None, old_read=False):
    S_list = np.linspace(-3, 0, 40)

    conv_time = []
    conv_time_std = []
    active = []
    active_std = []
    coop = []
    coop_std = []
    for S in S_list:
        try:
            if not old_read:
                conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=S, T=T)
                res, conf = read_stationary_generic(conf, directory=res_dir)
            else:
                conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=None, T=T)
                res, conf = read_stationary_generic(conf, directory=res_dir)
                result = None
                for line in res:
                    if line['conf']['S'] == S:
                        result = line
                        break
                res = result
        except Exception:
            print('ERROR? WHY?')  # it's if the simulation didn't finish yet

        coop.append(np.mean(res['left_fraction']))
        coop_std.append(np.std(res['left_fraction']))
        active.append(np.mean(res['active_density']))
        active_std.append(np.std(res['active_density']))
        conv_time.append(np.mean(res['convergence_time']))
        conv_time_std.append(np.std(res['convergence_time']))

    plt.plot(S_list, conv_time, label=f'$k={av_degree}$', color=color)
    print(S_list)


if __name__ == '__main__':
    fig = plt.figure(figsize=(4, 3))
    # plt.axvline(-1, linestyle='-.', color='black', linewidth=0.9)
    # plt.axvline(-2, linestyle='-.', color='black', linewidth=0.9)

    # for UI
    # plt.axvline(-2, linestyle='-.', color='black', linewidth=0.9)
    # plt.axvline(-2.923076923076923, linestyle=':', color='black', linewidth=0.9)
    # plt.axvline(-2.4615384615384617, linestyle=':', color='black', linewidth=0.9)

    plt.axvline(-0.9230769230769229, linestyle='-.', color='black', linewidth=0.9)
    plt.axvline(-1.4615384615384615, linestyle=':', color='black', linewidth=0.9)
    plt.axvline(-1.923076923076923, linestyle=':', color='black', linewidth=0.9)
    plt.axvline(-2.76923077, linestyle=':', color='black', linewidth=0.9)
    plt.title('c', loc='left', fontweight='bold')

    # T = 0.0
    # T = -1.0
    T = 0.0769230769230771

    ax = plt.gca()
    # plt.text(0.05, 0.9, f"$T=-1$", fontsize=10, transform=ax.transAxes)
    # plt.text(0.8, 0.9, f"$T=0$", fontsize=10, transform=ax.transAxes)
    plt.text(0.77, 0.9, f"$T=0.08$", fontsize=10, transform=ax.transAxes)

    # type_ = const.REPLICATOR
    # for i, k in enumerate([8, 32, 128, 999]):
    #     plot_res(str_type=type_, av_degree=k, T=T, res_dir=f'repl_new_res{k}', color=COLORS[i])

    # type_ = const.BEST_RESPONSE
    # plot_res(str_type=type_, av_degree=8, T=T, res_dir='best_res', old_read=True, color=COLORS[0])
    # for i, k in enumerate([32, 128, 999]):
    #     plot_res(str_type=type_, av_degree=k, T=T, res_dir=f'best_res{k}', color=COLORS[i+1])

    type_ = const.UNCOND_IMITATION
    for i, k in enumerate([8, 32, 128, 999]):
        plot_res(str_type=type_, av_degree=k, T=T, res_dir=f'imit_new_res{k}', color=COLORS[i])

    ##########################################################

    plt.legend(loc=9)
    # plt.legend()
    plt.xlabel(r'$S$')
    plt.ylabel(r'$\tau$')
    plt.title(NAMES[type_])

    # plt.ylim(ymax=12.7)
    plt.xlim([-3, 0])

    left, bottom, width, height = [0.75, 0.3, 0.15, 0.12]

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"times_{NAMES2[type_]}_T{T}.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


