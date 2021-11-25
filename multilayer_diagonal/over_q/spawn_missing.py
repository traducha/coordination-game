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
    script = f'run_over_nov.py'

    ###########################################
    update_str_type = const.REPLICATOR
    ###########################################
    k = 8
    ###########################################
    # T1 = -1
    # S1 = -2
    # T2 = -1
    # S2 = -2
    ###########################################
    node_overlap_list = np.linspace(0, 1, 30)
    ###########################################

    for T1 in np.linspace(-1, -3, 11)[1:]:
        T1 = round(T1, 2)
        T2 = round(-2.0 - T1, 2)
        S1 = round(-T1 - 3.0, 2)
        S2 = round(-T2 - 3.0, 2)

        results_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{round(T2-T1, 2)}"
        os.makedirs(results_dir, exist_ok=True)

        for i, node_overlap in enumerate(node_overlap_list):
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
                print(f'Results for q={node_overlap} already exist.')
            else:
                out_file = f'{results_dir}/out_nov{node_overlap}.txt'
                er_file = f'{results_dir}/error_nov{node_overlap}.txt'
                command = f'run -t 10:00 -o {out_file} -e {er_file} {py_path} {script} {node_overlap} {update_str_type} {results_dir} {T1} {S1} {T2} {S2} {k}'
                os.system(command)
