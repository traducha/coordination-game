# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": None,
    "payoff_type": const.COMPLEX,
    "b": 1.5,  # necessary for the complex payoff matrix
    "R": None,  # parameters for the general payoff matrix
    "P": None,
    "S": None,
    "T": None,
    "update_str_type": None,
    "loop_type": const.ASYNC,
    "loop_length": 10000,
    "number_of_loops": 100,
    "check_frozen": True,
    "sample_size": 100,
    "multilayer": None
}
