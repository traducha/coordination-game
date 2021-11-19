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
    update_str_type = const.REPLICATOR
    ###########################################
    k = 8
    ###########################################
    T1 = -1
    S1_list = np.linspace(-0.95, 0.0, 20)
    T2 = -1
    S2_list = np.linspace(-3.05, -4.0, 20)
    ###########################################
    node_overlap = 1.0
    ###########################################

    for S1, S2 in zip(S1_list, S2_list):
        S1 = round(S1, 2)
        S2 = round(S2, 2)
        results_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{round(S1 - S2, 2)}"
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
