# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from pprint import pprint
import igraph as ig
import numpy as np
import json
import time
import sys
import os


def run_with_time(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()

        minutes = (end_time - start_time) / 60.0
        if minutes <= 60:
            print(f'Function <{func.__name__}> finished in {round(minutes, 0)} min')
        else:
            print(f'Function <{func.__name__}> finished in {round(minutes / 60, 1)} h')
    return inner

# writing reading res, plotting etc
