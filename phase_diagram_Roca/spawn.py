# -*- coding: utf-8 -*-
import numpy as np
import os


if __name__ == '__main__':
    py_path = '/home/tomasz/anaconda2/envs/conda_python3.6/bin/python3'

    ###########################################
    script = 'run_over_S_imit.py'
    ###########################################

    processes = 12
    results_dir = "imitation_res"
    os.makedirs(results_dir, exist_ok=True)

    T_list = np.linspace(-2, 1, 40)
    for i, T in enumerate(T_list):
        out_file = f'{results_dir}/out_T{T}.txt'
        er_file = f'{results_dir}/error_T{T}.txt'
        command = f'run -x -c {processes} -o {out_file} -e {er_file} {py_path} {script} {T} {processes} {results_dir}'
        os.system(command)
