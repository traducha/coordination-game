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
from tools import read_stationary_generic
from config import config_values


# COLORS = [const.ORANGE, const.GREEN_DARK, const.VIOLET]
COLORS = [const.YELLOW, const.ORANGE, const.REDISH, const.GREEN_DARK, const.BLUE, const.VIOLET][::-1]

NAMES = {
    const.BEST_RESPONSE: 'BR',
    const.UNCOND_IMITATION: 'UI',
    const.REPLICATOR: 'RD',
}

NAMES15 = {
    const.BEST_RESPONSE: 'b',
    const.UNCOND_IMITATION: 'c',
    const.REPLICATOR: 'a',
}

NAMES2 = {
    const.BEST_RESPONSE: 'best',
    const.UNCOND_IMITATION: 'ui',
    const.REPLICATOR: 'repl',
}


def func(x, a, b, c, d, e):
    return e * (x**4.0) + a * (x**3.0) + b * (x**2.0) + c * x + d


def func3(x, b, c):
    return (x ** b) * c


def func4(x, a, b, c):
    return a * np.log(x + b) + c


def plot_res(str_type=const.UNCOND_IMITATION, N_list=(500, 1000, 2000, 4000, 8000, 16000),
             res_dir='res_imit_n'):

    fig = plt.figure(figsize=(4, 3))
    plt.axhline(0.5, linestyle='--', color='#bbbbbb')

    k_list = list(range(1, 61))
    max_time_list = []
    times = []
    fit_kc = []

    for i, N in enumerate(N_list):
        conv_time = []
        coop_up = []
        coop_up_std = []
        coop_down = []
        max_time = float('-inf')
        k_c = None
        for k in k_list:
            try:
                conf = dict(config_values, update_str_type=str_type, av_degree=k, num_nodes=N)
                res, conf = read_stationary_generic(conf, directory=''.join([res_dir, str(N), '']))
            except Exception:
                print('ERROR? WHY?')  # it's if the simulation didn't finish yet

            array = np.array(res['left_fraction'])
            up = array[array > 0.5]
            down = array[array <= 0.5]
            if len(up) == 0:
                up = [0.5]
            coop_up.append(np.mean(up))
            coop_up_std.append(np.std(up))
            coop_down.append(np.mean(down))
            conv_time.append(np.mean(res['convergence_time']))
            if conv_time[-1] > max_time:
                max_time = conv_time[-1]
                k_c = k

        times.append(conv_time)
        max_time_list.append(k_c)

        plt.scatter(k_list, conv_time, label=f'$N={N}$', color=COLORS[i], facecolor='none')

        od = 4
        do = 18
        popt, pcov = curve_fit(func, k_list[od:do], conv_time[od:do])
        plt.plot(np.linspace(5.5, 17, 100), func(np.linspace(5.5, 17, 100), *popt), color='black', linewidth=1)

        max_fit_kc = 4
        for real_k in np.linspace(5.5, 17, 1000):
            if func(real_k, *popt) > func(max_fit_kc, *popt):
                max_fit_kc = real_k
        fit_kc.append(max_fit_kc)
        # plt.axvline(max_fit_kc)

    print(max_time_list)
    print(fit_kc)

    # plt.legend(loc=5, fontsize=7)
    plt.xlabel(r'$k$')
    plt.ylabel(r'$\alpha$')
    plt.title(f"{NAMES[conf['update_str_type']]}")
    plt.title(f"{NAMES15[conf['update_str_type']]}", loc='left', fontweight='bold')

    plt.xlim([0, 60])
    # plt.ylim([0, 1])

    left, bottom, width, height = [0.6, 0.5, 0.3, 0.3]
    ax3 = fig.add_axes([left, bottom, width, height])
    ax3.patch.set_alpha(0.4)
    # ax3.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax3.scatter(N_list, fit_kc, s=16, marker='o', color=const.VIOLET, facecolor='none')

    popt, pcov = curve_fit(func3, N_list, fit_kc)
    print(popt)
    ax3.plot(np.linspace(400, 20000, 100), func3(np.linspace(400, 20000, 100), *popt), color='blue', linewidth=1)
    residuals = np.array(fit_kc) - func3(np.array(N_list), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(fit_kc) - np.mean(np.array(fit_kc))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('power law', r_squared)

    popt, pcov = curve_fit(func4, N_list, fit_kc)
    print(popt)
    ax3.plot(np.linspace(400, 20000, 100), func4(np.linspace(400, 20000, 100), *popt), color='black', linewidth=1)
    residuals = np.array(fit_kc) - func4(np.array(N_list), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(fit_kc) - np.mean(np.array(fit_kc))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('logarithmic', r_squared)

    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlim([400, 20000])
    # ax3.set_ylim([15, 47])
    ax3.tick_params(axis='both', which='major', labelsize=8)
    ax3.tick_params(axis='both', which='minor', labelsize=8)


    plt.tight_layout()

    plot_name = f"simple_{NAMES2[conf['update_str_type']]}_scaling.png"
    # plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


