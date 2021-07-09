# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": None,
    "payoff_type": const.GENERIC,
    "b": None,  # necessary for the complex payoff matrix
    "R": 1,  # parameters for the general payoff matrix
    "P": 0,
    "S": None,
    "T": -1,
    "update_str_type": None,
    "loop_type": const.ASYNC,
    "loop_length": 10000,
    "number_of_loops": 100,
    "check_frozen": True,
    "sample_size": 100,
    "multilayer": None
}
