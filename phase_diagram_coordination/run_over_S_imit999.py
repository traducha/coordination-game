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

import logging as log  # TODO make it importable

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)


@run_with_time
def main(configuration, directory=None):

    conv_time, left_nums, active_nums = get_stationary_state_sample(**configuration)
    res = {
        'conf': configuration,
        'convergence_time': conv_time,
        'active_density': active_nums,
        'left_fraction': left_nums,
    }

    save_stationary_generic(configuration, res, directory=directory)
    # res, conf = read_stationary_generic(configuration, directory=directory)
    # plot_over_two_params(res, 'S', 'T', conf)


if __name__ == '__main__':
    T = float(sys.argv[1])
    S = float(sys.argv[2])
    dir_name = str(sys.argv[3])
    log.info(f'T={T}, S={S}, dir_name={dir_name}')

    for update_type in [const.UNCOND_IMITATION]:
        config = dict(config_values, update_str_type=update_type, T=T, S=S, av_degree=999)
        log.info('Configuration: ')
        pprint(config)
        main(config, directory=dir_name)
