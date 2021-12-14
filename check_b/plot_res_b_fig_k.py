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


COLORS = ['#505050', const.YELLOW, const.ORANGE, const.REDISH, const.GREEN_DARK, const.BLUE, const.VIOLET]
k3_s_list = [10., 9.55102041, 9.10204082, 8.65306122, 8.20408163,
             7.75510204, 7.30612245, 6.85714286, 6.40816327, 5.95918367,
             5.51020408, 5.06122449, 4.6122449, 4.16326531, 3.71428571,
             3.26530612, 2.81632653, 2.36734694, 1.91836735, 1.46938776,
             1.02040816, 0.57142857, 0.12244898, -0.32653061, -0.7755102,
             -1.2244898, -1.67346939, -2.12244898, -2.57142857, -3.02040816,
             -3.46938776, -3.91836735, -4.36734694, -4.81632653, -5.26530612,
             -5.71428571, -6.16326531, -6.6122449, -7.06122449, -7.51020408,
             -7.95918367, -8.40816327, -8.85714286, -9.30612245, -9.75510204,
             -10.20408163, -10.65306122, -11.10204082, -11.55102041, -12]
k3_coop = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
           1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5900000000000001, 0.60325, 0.29359999999999997, 0.3102499999999999,
           0.30905000000000005, 0.22619999999999996, 0.23099999999999998, 0.18554999999999988, 0.18904999999999994,
           0.18359999999999999, 0.18290000000000006, 0.19679999999999997, 0.19120000000000004, 0.18819999999999992,
           0.19630000000000014, 0.1816500000000001, 0.1935499999999999, 0.18789999999999996, 0.1877000000000001,
           0.1874, 0.19159999999999988, 0.1861999999999998, 0.19515000000000016]


def func(x, b, c):
    return (x ** b) * c


def plot_res(str_type=const.UNCOND_IMITATION, av_degrees=[8, 32, 100, 250, 500, 999, 3]):
    fig = plt.figure(figsize=(4, 3.2))
    ax1 = fig.add_subplot(111)
    ax1.set_xticks([-10, -5, 0, 5])
    plt.axvline(-2, linestyle='--', color='black', linewidth=0.9)

    b_list = np.linspace(-9, 11, 100)
    s_list = [-x-1.0 for x in b_list]

    handles = []
    for i, k in enumerate(av_degrees[::-1]):
        if k == 3:
            handel, = plt.plot(k3_s_list, k3_coop, color=COLORS[i], label=f'$k={k}$')
            handles.append(handel)
        else:
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

    handles = handles[1:] + [handles[0]]
    ################################################################################
    ################################################################################

    plt.legend(loc=2, handles=handles[::-1], fontsize=8.27)
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

    plot_name = f"imit_S_b_k.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


