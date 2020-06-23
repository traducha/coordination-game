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
from tools import run_with_time
from networks import initialize_random_reg_net
from main import run_trajectory

sys.path.insert(1, sys.path[0])
from config import config_values


# TODO functions for saving and reading every result (and plot)
# functions to get only final values to make plots vs params


def save_trajectory(config, time_steps, active_nums, left_nums, convergence_time):
    os.makedirs('results', exist_ok=True)
    results = {
        'convergence_time': convergence_time,
        'time_steps': time_steps,
        'active_density': active_nums,
        'left_fraction': left_nums,
    }

    to_write = {'config': config,
                'results': results}

    f_name = f'trajectory_N{}_k{}_.json'  # TODO translate config into suffix
    with open(f_name, 'w') as out_file:
        json.dump(to_write, out_file, indent=4)


@run_with_time
def main():
    convergence_t, time_steps, active_nums, left_nums = run_trajectory(**config_values)

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
