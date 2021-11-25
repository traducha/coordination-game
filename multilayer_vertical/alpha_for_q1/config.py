# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": None,
    "payoff_type": const.GENERIC,
    "b": None,  # necessary for the complex payoff matrix
    "R": None,  # parameters for the general payoff matrix
    "P": None,
    "S": None,
    "T": None,
    "update_str_type": None,
    "loop_type": const.ASYNC,
    "loop_length": 100000,
    "number_of_loops": 10,
    "check_frozen": True,
    "sample_size": 2000,
    "multilayer":
        {
            "num_layers": 2,
            "to_rewire": 0,
            "rewire_first_layer": False,
            "shared_nodes_ratio": None,
            "layers_config": [
                {"b": None, "R": 1, "P": 0, "S": None, "T": None},
                {"b": None, "R": 1, "P": 0, "S": None, "T": None},
            ],
        },
}
