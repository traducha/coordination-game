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
    script = 'run_new_big.py'
    ###########################################
    update_str_type = const.REPLICATOR
    ###########################################
    results_dir = "repl_new_res8_big"
    ###########################################
    av_degree = 8
    ###########################################
    T_list = np.linspace(-2, 1, 40)
    S_list = np.linspace(-3, 0, 40)

    os.makedirs(results_dir, exist_ok=True)

    for i, T in enumerate(T_list):
        for j, S in enumerate(S_list):
            out_file = f'{results_dir}/out_T{T}_S{S}.txt'
            er_file = f'{results_dir}/error_T{T}_S{S}.txt'
            command = f'run -t 300:59 -o {out_file} -e {er_file} {py_path} {script} {T} {S} {results_dir} {update_str_type} {av_degree}'
            os.system(command)
