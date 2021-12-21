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
from tools import read_stationary_generic, read_trajectory
from config import config_values

COLORS = [const.GREEN_DARK, const.YELLOW, const.VIOLET, const.ORANGE, const.BLUE, const.REDISH, const.GREEN_BRIGHT]


def plot_res():
    fig = plt.figure(figsize=(4, 3))

    plt.xlabel(r'$t$')
    plt.ylabel(r'$\alpha$')
    plt.xlim([0, 15])
    plt.ylim([-0.0, 1.0])
    plt.title("b", loc='left', fontweight='bold')
    plt.title("BR")

    for i, k in enumerate([2, 4, 5, 6, 8, 15, 20]):
        file_name = f'trajectory_n1000_k{k}_bNone_RNone_PNone_TNone_SNone_pay1_up4_loo5_len10_num50000_che1_sam500.json'
        with open(('trajectories/' + file_name), 'r') as in_file:
            from_file = json.load(in_file)
        res, conf = from_file['results'], from_file['config']
        plt.plot(res['time_steps'], res['left_fraction'], label=f'$k={k}$', color=COLORS[i])

    plt.legend(fontsize=9)
    # plt.gcf().subplots_adjust(top=1, bottom=0.8, right=1, left=0.09)
    plt.tight_layout()

    plot_name = f"simple_best_traj_only.pdf"
    plt.savefig(plot_name)
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_res()


