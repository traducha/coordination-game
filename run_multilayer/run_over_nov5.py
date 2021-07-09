# -*- coding: utf-8 -*-
from pprint import pprint
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, log
from main import get_stationary_state_sample
from config5 import config_values


@run_with_time
def main(configuration, directory):
    conv_time, left_nums, active_nums = get_stationary_state_sample(multi=True, **configuration)
    res = {
        'conf': configuration,
        'convergence_time': conv_time,
        'active_density': active_nums,
        'left_fraction': left_nums,
    }

    save_stationary_generic(configuration, res, directory=directory)


if __name__ == '__main__':
    nov = float(sys.argv[1])
    update_str_type = int(sys.argv[2])
    dir_name = str(sys.argv[3])
    log.info(f'nov={nov}, update_str_type={update_str_type}, dir_name={dir_name}')

    multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov)
    conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type)

    log.info(f'Configuration: ')
    pprint(conf)
    main(conf, dir_name)
