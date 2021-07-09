# -*- coding: utf-8 -*-
from pprint import pprint
import numpy as np
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, log
from main import get_stationary_state_sample
import constants as const
from config import config_values


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


if __name__ == '__main__':
    T = float(sys.argv[1])
    S = float(sys.argv[2])
    dir_name = str(sys.argv[3])
    update_str_type = int(sys.argv[4])
    log.info(f'T={T}, S={S}, dir_name={dir_name}')

    config = dict(config_values, update_str_type=update_str_type, T=T, S=S)
    log.info('Configuration: ')
    pprint(config)
    main(config, directory=dir_name)
