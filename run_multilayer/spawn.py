# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
sys.path.insert(1, '/home/tomasz/PycharmProjects/cooperation-game')
sys.path.insert(1, sys.path[0])
import constants as const


if __name__ == '__main__':
    py_path = '/home/tomasz/anaconda2/envs/conda_python3.6/bin/python3'

    ###########################################
    script = 'run_over_nov_av100.py'
    ###########################################
    results_dir = "res_ui_nov_av100"
    ###########################################
    update_str_type = const.UNCOND_IMITATION
    ###########################################
    node_overlap_list = np.linspace(0, 1, 30)
    ###########################################

    os.makedirs(results_dir, exist_ok=True)

    for i, node_overlap in enumerate(node_overlap_list):
        out_file = f'{results_dir}/out_nov{node_overlap}.txt'
        er_file = f'{results_dir}/error_nov{node_overlap}.txt'
        command = f'run -x -o {out_file} -e {er_file} {py_path} {script} {node_overlap} {update_str_type} {results_dir}'
        os.system(command)
