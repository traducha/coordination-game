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


def plot_res():
    fig = plt.figure(figsize=(4, 3))

    N_list = [500, 1000, 2000, 4000, 8000, 16000]
    tau_max = [6, 6, 6, 6, 6, 6]
    tau_std = [0.046153526582483374, 0.0342770568164771, 0.023891673256597162, 0.01720371805017741, 0.01185484104701535, 0.008471981649088956]
    alpha_max = [7, 7, 7, 7, 7, 7]
    alpha_std = [0.04305835500805853, 0.03133776322585898, 0.021340307776599662, 0.015907341473357515, 0.011326781040966584, 0.007556722520378793]

    plt.plot(N_list, alpha_max, color=const.ORANGE)
    plt.scatter(N_list, alpha_max, color=const.ORANGE, label=r'$\alpha_{max}$')
    plt.plot(N_list, tau_max, color=const.BLUE)
    plt.scatter(N_list, tau_max, color=const.BLUE, label=r'$\tau_{max}$', marker='p')

    plt.title(r'$k_c$ for CCG with $b=5$')
    plt.xlabel(r'$N$')
    plt.ylabel(r'$k_c$')
    plt.legend()

    plt.xscale('log')
    # plt.yscale('log')
    plt.ylim([2, 8])
    plt.xlim([400, 20000])

    left, bottom, width, height = [0.55, 0.3, 0.37, 0.25]
    ax2 = fig.add_axes([left, bottom, width, height])

    ax2.plot(N_list, alpha_std, color=const.ORANGE, linestyle='--')
    ax2.scatter(N_list, alpha_std, color=const.ORANGE, label=r'$~~\alpha$ std', facecolors='none')
    ax2.plot(N_list, tau_std, color=const.BLUE, linestyle='--')
    ax2.scatter(N_list, tau_std, color=const.BLUE, label=r'$~~\tau$ std', facecolors='none', marker='p')

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_ylim([0.005, 0.1])
    ax2.legend(handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    plt.tight_layout()

    plot_name = f"ccg_b5_ui_scaling.png"
    # plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


