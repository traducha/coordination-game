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
    script = 'run_over_S_new.py'
    ###########################################
    results_dir = "res_S500_new"
    ###########################################
    S_list = np.linspace(-12, 8, 100)
    ###########################################

    os.makedirs(results_dir, exist_ok=True)

    for i, S in enumerate(S_list):
        out_file = f'{results_dir}/out_S{S}.txt'
        er_file = f'{results_dir}/error_S{S}.txt'
        command = f'run -x -t 100:59 -o {out_file} -e {er_file} {py_path} {script} {S} {results_dir}'
        # print(command)
        os.system(command)
