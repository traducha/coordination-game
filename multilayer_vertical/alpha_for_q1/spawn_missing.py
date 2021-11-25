# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
import constants as const
from tools import rules_dicts as rules, config_into_suffix
from config import config_values


if __name__ == '__main__':
    py_path = '/home/tomasz/anaconda2/envs/conda_python3.6/bin/python3'
    script = f'run.py'

    ###########################################
    update_str_type = const.BEST_RESPONSE
    ###########################################
    k = 8
    ###########################################
    T1_list = np.linspace(-1.05, -3.0, 40)
    S1 = -2
    T2_list = np.linspace(-0.95, 1.0, 40)
    S2 = -2
    ###########################################
    node_overlap = 1.0
    ###########################################

    for T1, T2 in zip(T1_list, T2_list):
        T1 = round(T1, 2)
        T2 = round(T2, 2)
        results_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{round(T2 - T1, 2)}"
        os.makedirs(results_dir, exist_ok=True)

        # prepare configuration
        layers_config = config_values['multilayer']['layers_config']
        layers_config[0]['T'] = T1
        layers_config[0]['S'] = S1
        layers_config[1]['T'] = T2
        layers_config[1]['S'] = S2

        multi_conf = dict(config_values['multilayer'], shared_nodes_ratio=node_overlap, layers_config=layers_config)
        conf = dict(config_values, multilayer=multi_conf, update_str_type=update_str_type, av_degree=k)

        f_name = f'{results_dir}/stationary_generic_{config_into_suffix(conf)}.json'
        if os.path.isfile(f_name):
            print(r'Results for $\Delta S$=' + f'{round(S1 - S2, 2)} already exist.')
        else:
            out_file = f'{results_dir}/out_nov{node_overlap}.txt'
            er_file = f'{results_dir}/error_nov{node_overlap}.txt'
            command = f'run -t 16:00 -o {out_file} -e {er_file} {py_path} {script} {node_overlap} {update_str_type} {results_dir} {T1} {S1} {T2} {S2} {k}'
            os.system(command)
