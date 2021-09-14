# -*- coding: utf-8 -*-
from pprint import pprint
import sys

sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
from tools import run_with_time, save_stationary_generic, log
from constants import rules_names as rules
from main import get_stationary_state_sample
from config import config_values


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
    T1 = float(sys.argv[4])
    S1 = float(sys.argv[5])
    T2 = float(sys.argv[6])
    S2 = float(sys.argv[7])
    log.info(f'nov={nov}, update_str_type={rules[update_str_type]}, dir_name={dir_name}')

    layers_config = config_values['multilayer']['layers_config']
    layers_config[0]['T'] = T1
    layers_config[0]['S'] = S1
    layers_config[1]['T'] = T2
    layers_config[1]['S'] = S2

    multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=nov, layers_config=layers_config)
    conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=8)

    log.info(f'Configuration: ')
    pprint(conf)
    main(conf, dir_name)
