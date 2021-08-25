# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import read_stationary_generic
from config2 import config_values


COLORS = [const.YELLOW, const.ORANGE, const.REDISH, const.GREEN_DARK, const.BLUE, const.VIOLET]


def func(x, b, c):
    return (x ** b) * c


def plot_res(str_type=const.UNCOND_IMITATION, av_degrees=[8, 32, 100, 250, 500, 999]):
    fig = plt.figure(figsize=(4, 3.2))
    ax1 = fig.add_subplot(111)
    ax1.set_xticks([-10, -5, 0, 5])
    plt.axvline(-2, linestyle='--', color='black', linewidth=0.9)

    b_list = np.linspace(-9, 11, 100)
    s_list = [-x-1.0 for x in b_list]

    handles = []
    for i, k in enumerate(av_degrees[::-1]):
        coop = []
        coop_std = []
        for b in b_list:
            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k, b=b,
                            num_nodes=1000, sample_size=100)
                res, conf = read_stationary_generic(conf, directory=f'res_b{k}_new')
            except Exception:
                raise

            coop.append(1.0-np.mean(res['left_fraction']))
            coop_std.append(np.std(res['left_fraction']))

        handel, = plt.plot(s_list, coop, color=COLORS[i], label=f'$k={k}$')
        handles.append(handel)

    ################################################################################
    ################################################################################

    plt.legend(loc=2, handles=handles[::-1])
    plt.xlabel(r'$S$')
    plt.xlim([-12, 8])
    plt.ylim([-0.05, 1.05])
    plt.title('b', loc='left', fontweight='bold')

    _ax1 = ax1.twiny()
    _ax1.set_xlim(ax1.get_xlim())
    new_ticks = [-11, -6, -1, 4]
    _ax1.set_xticks(new_ticks)
    _ax1.set_xticklabels([-x-1 for x in new_ticks])
    _ax1.set_xlabel(r'$b$')

    #####################################################################
    #####################################################################

    left, bottom, width, height = [0.695, 0.38, 0.26, 0.24]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.patch.set_alpha(0.8)

    N_list = [500, 1000, 2000, 4000, 8000, 16000]
    alpha_std_8 = [0.04210867768049717, 0.029806016775141234, 0.021276573290828577,
                 0.014037775144231369, 0.010186640451468776, 0.007019907490264737]
    alpha_std_32 = [0.006566917084903686, 0.005444099925607542, 0.004244464041548704,
                    0.002298184065735374, 0.0019362937535405246, 0.0012999068716642722]

    # ax2.plot(N_list, alpha_std_8, color=const.VIOLET, linestyle='-')
    popt, pcov = curve_fit(func, N_list, alpha_std_8, maxfev=2000)
    print('power=', popt[0])
    ax2.plot(np.linspace(490, 16500, 100), func(np.linspace(490, 16500, 100), *popt), color='black', linewidth=1)
    residuals = np.array(alpha_std_8) - func(np.array(N_list), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(alpha_std_8) - np.mean(np.array(alpha_std_8))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('k8 R^2', r_squared)

    ax2.scatter(N_list, alpha_std_8, color=const.VIOLET, label=r'$\alpha$ std', facecolors='none', marker='o')
    ax2.text(4000, 0.025, f"$k$=8", fontsize=8)

    # ax2.plot(N_list, alpha_std_32, color=const.BLUE, linestyle='-')
    popt, pcov = curve_fit(func, N_list, alpha_std_32, maxfev=2000)
    print('power=', popt[0])
    ax2.plot(np.linspace(490, 16500, 100), func(np.linspace(490, 16500, 100), *popt), color='black', linewidth=1)
    residuals = np.array(alpha_std_32) - func(np.array(N_list), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(alpha_std_32) - np.mean(np.array(alpha_std_32))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('k8 R^2', r_squared)

    ax2.scatter(N_list, alpha_std_32, color=const.BLUE, label=r'$\alpha$ std', facecolors='none', marker='D', s=27)
    ax2.text(600, 0.0015, f"$k$=32", fontsize=8)

    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.tick_params(axis='both', which='minor', labelsize=8)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_ylim([0.001, 0.1])
    ax2.set_xlabel(r'$N$')
    ax2.set_ylabel(r'$\alpha_{std}$')
    ax2.xaxis.labelpad = -2
    ax2.yaxis.labelpad = 1

    plt.tight_layout()

    plot_name = f"imit_S_b_k.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


