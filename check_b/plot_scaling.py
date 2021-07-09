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


def b_to_S(b_list):
    return [-b-1 for b in b_list]


def plot_res():
    fig = plt.figure(figsize=(4, 3))

    k_list = [8, 20, 32, 44, 56, 68, 80, 90, 100, 250, 500, 999]
    b_c_1000 = b_to_S([2.8181818181818175, 2.206896551724138, 2.1111111111111107, 1.9310344827586206, 1.793103448275862,
                1.6551724137931034, 1.5862068965517242, 1.5172413793103448, 1.5050505050505052, 1.3030303030303028,
                1.2020202020202015, 1])
    b_c_4000 = b_to_S([2.8894736842105266, 2.2263157894736842, 1.9838709677419355, 1.8767441860465115, 1.7781818181818183,
                1.6736842105263159, 1.6184210526315792, 1.5631578947368423, 1.5078947368421054, 1.3421052631578947,
                1.2142857142857144])
    b_c_8000 = b_to_S([2.896551724137931, 2.206896551724138, 2.0, 1.9310344827586206, 1.793103448275862, 1.7241379310344827,
                1.6551724137931034, 1.5862068965517242, 1.5172413793103448, 1.3321428571428573, 1.2142857142857144])

    plt.axhline(-2, linestyle='--', color='black', linewidth=0.9)
    plt.plot(k_list, b_c_1000, color=const.GREEN)
    plt.scatter(k_list, b_c_1000, color=const.GREEN, facecolor='None', label=r'$N=1000$')
    plt.plot(k_list[:-1], b_c_4000, color=const.BLUE)
    plt.scatter(k_list[:-1], b_c_4000, color=const.BLUE, marker='s', facecolor='None', label=r'$N=4000$')
    plt.plot(k_list[:-1], b_c_8000, color=const.REDISH)
    plt.scatter(k_list[:-1], b_c_8000, color=const.REDISH, marker='v', facecolor='None', label=r'$N=8000$')

    # plt.title(r'$b_c$ scaling for CCG with UI')
    plt.figtext(0.23, 0.8, 'c', fontsize=12, weight='bold')
    plt.xlabel(r'$k$')
    plt.ylabel(r'$S_c$')
    plt.legend()

    # plt.xscale('log')
    # plt.yscale('log')
    # plt.ylim([2, 8])
    plt.xlim([-50, 1050])

    # left, bottom, width, height = [0.65, 0.35, 0.25, 0.25]
    # ax2 = fig.add_axes([left, bottom, width, height])
    #
    # # ax2.plot(k_list, b_c_1000, color=const.GREEN)
    # ax2.scatter(k_list, b_c_1000, color=const.GREEN, facecolor='None', label=r'$N=1000$')
    # # ax2.plot(k_list, b_c_4000, color=const.BLUE)
    # ax2.scatter(k_list[:-1], b_c_4000, color=const.BLUE, marker='s', facecolor='None', label=r'$N=4000$')
    # # ax2.plot(k_list, b_c_8000, color=const.REDISH)
    # ax2.scatter(k_list[:-1], b_c_8000, color=const.REDISH, marker='v', facecolor='None', label=r'$N=8000$')
    #
    # ax2.set_xscale('log')
    # ax2.set_yscale('log')
    # ax2.set_xlim([5, 1400])
    # ax2.set_ylim([0.9, 3.3])
    # ax2.tick_params(axis='both', which='major', labelsize=8)
    # ax2.tick_params(axis='both', which='minor', labelsize=8)

    plt.tight_layout()

    plot_name = f"ccg_bc_ui_scaling.png"
    # plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


