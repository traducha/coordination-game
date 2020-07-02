# -*- coding: utf-8 -*-
from pprint import pprint
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_over_param, read_stationary_over_param, plot_over_param
from main import get_stationary_state_sample
import constants as const
from config import config_values


@run_with_time
def main(configuration):
    res = {}
    for b in np.linspace(0, 4, 10):
        conf = dict(configuration, b=b)
        conv_time, left_nums, active_nums = get_stationary_state_sample(**conf)
        res[b] = {
            'convergence_time': conv_time,
            'active_density': active_nums,
            'left_fraction': left_nums,
        }

    save_stationary_over_param(configuration, res, 'b')
    res, param, conf = read_stationary_over_param(configuration)
    plot_over_param(res, param, conf)


if __name__ == '__main__':
    print('Configuration: ')
    pprint(config_values)
    main(config_values)
