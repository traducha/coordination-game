# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from pprint import pprint
import igraph as ig
import numpy as np
import json
import time
import sys
import os

import constants as const
from tools import run_with_time, save_trajectory, config_into_suffix, read_trajectory
from networks import initialize_random_reg_net
from main import run_trajectory

sys.path.insert(1, sys.path[0])
from config import config_values


# TODO functions to get only final values to make plots vs params


@run_with_time
def main():
    convergence_t, time_steps, active_nums, left_nums = run_trajectory(**config_values)
    save_trajectory(config_values, time_steps, active_nums, left_nums, convergence_t)
    res, conf = read_trajectory(config_values)
    # TODO plotting from readed data

    plt.plot(time_steps, left_nums, label='left frac')
    plt.plot(time_steps, active_nums, label='active edges')
    plt.axvline(convergence_t)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print('Configuration: ')
    pprint(config_values)
    print()
    main()
