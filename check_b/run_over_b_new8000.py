# -*- coding: utf-8 -*-
from pprint import pprint
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
import constants as const
from tools import run_with_time, save_stationary_generic, log
from main import get_stationary_state_sample
from config2 import config_values


@run_with_time
def main(configuration, directory):
    conv_time, left_nums, active_nums = get_stationary_state_sample(multi=False, **configuration)
    res = {
        'conf': configuration,
        'convergence_time': conv_time,
        'active_density': active_nums,
        'left_fraction': left_nums,
    }

    save_stationary_generic(configuration, res, directory=directory)


if __name__ == '__main__':
    b = float(sys.argv[1])
    dir_name = str(sys.argv[2])
    av_degree = int(sys.argv[3])
    update_str_type = int(sys.argv[4])
    log.info(f'b={b}, k={av_degree}, dir_name={dir_name}')

    conf = dict(config_values, b=b, num_nodes=8000, av_degree=av_degree, update_str_type=update_str_type)

    log.info(f'Configuration: ')
    pprint(conf)
    main(conf, dir_name)
