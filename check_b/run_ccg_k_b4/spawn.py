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
    script = 'run.py'
    ###########################################
    update_str_type = const.UNCOND_IMITATION
    ###########################################
    results_dir = "../run_ccg_k_b1.5/imit_res_n1000_b4"
    ###########################################
    num_nodes = 1000
    ###########################################
    k_list = list(range(101, 201))
    ###########################################

    os.makedirs(results_dir, exist_ok=True)

    for i, k in enumerate(k_list):
        out_file = f'{results_dir}/out_k{k}.txt'
        er_file = f'{results_dir}/error_k{k}.txt'
        command = f'run -t 4:00 -o {out_file} -e {er_file} {py_path} {script} {k} {num_nodes} {results_dir} {update_str_type}'
        print(command)
        os.system(command)
