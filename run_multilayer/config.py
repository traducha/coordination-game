# -*- coding: utf-8 -*-
import constants as const

config_values = {
    "num_nodes": 1000,
    "av_degree": 8,
    "payoff_type": const.GENERIC,
    "b": None,  # necessary for the complex payoff matrix
    "R": None,  # parameters for the general payoff matrix
    "P": None,
    "S": None,
    "T": None,
    "update_str_type": const.REPLICATOR,
    "loop_type": const.ASYNC,
    "loop_length": 5000,
    "number_of_loops": 100,
    "check_frozen": True,
    "sample_size": 100,
    "multilayer":
        {
            "num_layers": 2,
            "to_rewire": 0,
            "rewire_first_layer": False,
            "shared_nodes_ratio": 0.01,
            "layers_config": [
                {"b": None, "R": 1, "P": 0, "S": -1, "T": 1},
                {"b": None, "R": 1, "P": 0, "S": 0, "T": 0},
            ],
        },
}
