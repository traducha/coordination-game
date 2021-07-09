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


def plot_res(str_type=const.UNCOND_IMITATION, av_degree=8, res_dir='imit_new_res8', old_read=False):
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
                conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=S, T=-1.0)
                res, conf = read_stationary_generic(conf, directory=res_dir)
            else:
                conf = dict(config_values, update_str_type=str_type, av_degree=av_degree, S=None, T=-1.0)
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

    plt.plot(S_list, conv_time, label=f'$k={av_degree}$')


if __name__ == '__main__':
    fig = plt.figure(figsize=(4, 3))

    # type_ = const.UNCOND_IMITATION
    # plot_res(str_type=type_, av_degree=8, res_dir='imit_new_res8')
    # plot_res(str_type=type_, av_degree=32, res_dir='imit_new_res32')
    # plot_res(str_type=type_, av_degree=128, res_dir='imit_new_res128')
    # plot_res(str_type=type_, av_degree=999, res_dir='imit_new_res999')

    # type_ = const.REPLICATOR
    # plot_res(str_type=type_, av_degree=8, res_dir='repl_new_res8')
    # plot_res(str_type=type_, av_degree=32, res_dir='repl_new_res32')
    # plot_res(str_type=type_, av_degree=128, res_dir='repl_new_res128')
    # plot_res(str_type=type_, av_degree=999, res_dir='repl_new_res999')

    type_ = const.BEST_RESPONSE
    plot_res(str_type=type_, av_degree=8, res_dir='best_res', old_read=True)
    plot_res(str_type=type_, av_degree=32, res_dir='best_res32')
    plot_res(str_type=type_, av_degree=128, res_dir='best_res128')
    plot_res(str_type=type_, av_degree=999, res_dir='best_res999')

    plt.legend()
    plt.xlabel('S')
    plt.ylabel(r'$\tau$')
    plt.title(f"{NAMES[type_]}")

    left, bottom, width, height = [0.75, 0.3, 0.15, 0.12]

    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"times_{NAMES2[type_]}_T-1.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


