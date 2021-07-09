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
    script = 'run_erdos.py'
    ###########################################
    update_str_type = const.REPLICATOR
    ###########################################
    results_dir = "res_repl_n1000_er"
    ###########################################
    num_nodes = 1000
    ###########################################
    k_list = [2, 3]  # list(range(1, 61))
    ###########################################

    os.makedirs(results_dir, exist_ok=True)

    for i, k in enumerate(k_list):
        out_file = f'{results_dir}/out_k{k}.txt'
        er_file = f'{results_dir}/error_k{k}.txt'
        command = f'run -t 60:59 -o {out_file} -e {er_file} {py_path} {script} {k} {num_nodes} {results_dir} {update_str_type}'
        print(command)
        os.system(command)
