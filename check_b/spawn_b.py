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
    script = 'run_over_b_er.py'
    ###########################################
    update_str_type = const.REPLICATOR
    ###########################################
    results_dir = "repl_res_b_k8_new_er"
    ###########################################
    b_list = np.linspace(-9, 11, 100)  # np.linspace(0.9, 2, 15)  # np.linspace(-9, 11, 100)
    ###########################################
    av_degree = 8
    ###########################################

    os.makedirs(results_dir, exist_ok=True)

    for i, b in enumerate(b_list):
        out_file = f'{results_dir}/out_b{b}.txt'
        er_file = f'{results_dir}/error_b{b}.txt'
        command = f'run -t 06:00 -o {out_file} -e {er_file} {py_path} {script} {b} {results_dir} {av_degree} {update_str_type}'
        os.system(command)
