# -*- coding: utf-8 -*-
from pprint import pprint
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, read_stationary_generic, plot_over_two_params
from main import get_stationary_state_sample
import constants as const
from config import config_values


@run_with_time
def main(configuration):
    res = []
    for T in np.linspace(-2, 1, 40):
        for S in np.linspace(-3, 0, 40):
            conf = dict(configuration, T=T, S=S)
            conv_time, left_nums, active_nums = get_stationary_state_sample(**conf)
            res.append({
                'conf': conf,
                'convergence_time': conv_time,
                'active_density': active_nums,
                'left_fraction': left_nums,
            })

    save_stationary_generic(configuration, res)
    res, conf = read_stationary_generic(configuration)
    # plot_over_two_params(res, 'S', 'T', conf)


if __name__ == '__main__':
    for update_type in [const.UNCOND_IMITATION]:
        config = dict(config_values, update_str_type=update_type)
        print('Configuration: ')
        pprint(config)
        main(config)

