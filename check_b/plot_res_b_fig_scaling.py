# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

import constants as const

import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])


def func(x, b, c):
    return -(x ** b) * c


def b_to_S(b_list):
    return [-b-1 for b in b_list]


def plot_res():
    fig = plt.figure(figsize=(4, 3.1))
    ax1 = fig.add_subplot(111)

    k_list = [8, 20, 32, 44, 56, 68, 80, 90, 100, 250, 500, 999]
    b_c_1000 = [2.8181818181818175, 2.206896551724138, 2.1111111111111107, 1.9310344827586206, 1.793103448275862,
                1.6551724137931034, 1.5862068965517242, 1.5172413793103448, 1.5050505050505052, 1.3030303030303028,
                1.1010101010101003, 1]
    b_c_4000 = [2.8894736842105266, 2.2263157894736842, 1.9838709677419355, 1.8767441860465115, 1.7781818181818183,
                1.6736842105263159, 1.6184210526315792, 1.5631578947368423, 1.5078947368421054, 1.3421052631578947,
                (1.292857142857143+1.2142857142857144+1.2142857142857144)/3]
    b_c_8000 = [2.896551724137931, 2.206896551724138, 2.0, 1.9310344827586206, 1.793103448275862, 1.7241379310344827,
                1.6551724137931034, 1.5862068965517242, 1.5172413793103448, 1.3321428571428573, 1.292857142857143]

    plt.axhline(-2, linestyle='--', color='black', linewidth=0.9)
    plt.plot(k_list, b_to_S(b_c_1000), color=const.ORANGE)
    plt.scatter(k_list, b_to_S(b_c_1000), color=const.ORANGE, facecolor='None', label=r'$N=1000$')
    plt.plot(k_list[:-1], b_to_S(b_c_4000), color=const.GREEN_DARK)
    plt.scatter(k_list[:-1], b_to_S(b_c_4000), color=const.GREEN_DARK, marker='s', s=30, facecolor='None', label=r'$N=4000$')
    plt.plot(k_list[:-1], b_to_S(b_c_8000), color=const.VIOLET)
    plt.scatter(k_list[:-1], b_to_S(b_c_8000), color=const.VIOLET, marker='v', facecolor='None', label=r'$N=8000$')

    plt.title('c', loc='left', fontweight='bold')
    plt.xlabel(r'$k$')
    plt.ylabel(r'$S_c$')
    plt.legend(loc='upper right', bbox_to_anchor=(1, 0.88))

    plt.ylim([-4, -1.9])
    plt.xlim([-50, 1050])

    ###############################################################

    _ax1 = ax1.twinx()
    _ax1.set_ylim(ax1.get_ylim())
    new_ticks = [-4, -3, -2]
    _ax1.set_yticks(new_ticks)
    _ax1.set_yticks([-3.5, -2.5], minor=True)
    _ax1.set_yticklabels([-x - 1 for x in new_ticks])
    _ax1.set_ylabel(r'$b_c$')

    #################################################

    left, bottom, width, height = [0.4, 0.28, 0.25, 0.25]
    ax2 = fig.add_axes([left, bottom, width, height])

    popt, pcov = curve_fit(func, k_list[:-3], b_to_S(b_c_1000)[:-3], maxfev=2000)
    print('power=', popt[0])
    ax2.plot(np.linspace(8, 400, 100), func(np.linspace(8, 400, 100), *popt), color='black', linewidth=1)
    residuals = np.array(b_to_S(b_c_1000)[:-3]) - func(np.array(k_list[:-3]), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(b_to_S(b_c_1000)[:-3]) - np.mean(np.array(b_to_S(b_c_1000)[:-3]))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('1000 R^2', r_squared)

    popt, pcov = curve_fit(func, k_list[:-3], b_to_S(b_c_4000)[:-2], maxfev=2000)
    print('power=', popt[0])
    # ax2.plot(np.linspace(8, 400, 100), func(np.linspace(8, 400, 100), *popt), color='black', linewidth=1)
    residuals = np.array(b_to_S(b_c_4000)[:-2]) - func(np.array(k_list[:-3]), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(b_to_S(b_c_4000)[:-2]) - np.mean(np.array(b_to_S(b_c_4000)[:-2]))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('4000 R^2', r_squared)

    popt, pcov = curve_fit(func, k_list[:-3], b_to_S(b_c_8000)[:-2], maxfev=2000)
    print('power=', popt[0])
    # ax2.plot(np.linspace(8, 400, 100), func(np.linspace(8, 400, 100), *popt), color='black', linewidth=1)
    residuals = np.array(b_to_S(b_c_8000)[:-2]) - func(np.array(k_list[:-3]), *popt)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((np.array(b_to_S(b_c_8000)[:-2]) - np.mean(np.array(b_to_S(b_c_8000)[:-2]))) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('8000 R^2', r_squared)

    ax2.scatter(k_list, b_to_S(b_c_1000), color=const.ORANGE, facecolor='None', label=r'$N=1000$')
    ax2.scatter(k_list[:-1], b_to_S(b_c_4000), color=const.GREEN_DARK, marker='s', s=30, facecolor='None', label=r'$N=4000$')
    ax2.scatter(k_list[:-1], b_to_S(b_c_8000), color=const.VIOLET, marker='v', facecolor='None', label=r'$N=8000$')

    ax2.set_xscale('symlog')
    ax2.set_yscale('symlog')
    ax2.set_yticks([-2, -3])
    ax2.set_yticks([-2.5, -3.5], minor=True)
    ax2.set_yticklabels([r'$-2$', r'$-3$'])
    # ax2.set_xlim([5, 1400])
    # ax2.set_ylim([0.9, 3.3])
    ax2.tick_params(axis='both', which='major', labelsize=8)
    ax2.tick_params(axis='both', which='minor', labelsize=8)

    plt.tight_layout()

    plot_name = f"imit_S_b_scaling.png"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


