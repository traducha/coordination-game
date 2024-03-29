# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
import constants as const
from tools import rules_dicts as rules


if __name__ == '__main__':
    py_path = '/home/tomasz/anaconda2/envs/conda_python3.6/bin/python3'
    script = f'run_over_nov.py'

    ###########################################
    update_str_type = const.BEST_RESPONSE
    ###########################################
    k = 8
    ###########################################
    T1 = -1
    S1 = -1.8
    T2 = -1
    S2 = -2.2
    ###########################################
    node_overlap_list = np.linspace(0, 1, 30)
    ###########################################

    results_dir = f"res/res_{rules[update_str_type]}_k{k}_gap{S1-S2}"
    os.makedirs(results_dir, exist_ok=True)

    for i, node_overlap in enumerate(node_overlap_list):
        if node_overlap == 0.0 or node_overlap > 0.37:
            t = '01'
        else:
            t = '07'

        out_file = f'{results_dir}/out_nov{node_overlap}.txt'
        er_file = f'{results_dir}/error_nov{node_overlap}.txt'
        command = f'run -t {t}:00 -o {out_file} -e {er_file} {py_path} {script} {node_overlap} {update_str_type} {results_dir} {T1} {S1} {T2} {S2} {k}'
        os.system(command)
