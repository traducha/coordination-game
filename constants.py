# -*- coding: utf-8 -*-

# colors for plotting
GOLD = '#D4AF37'
GREEN = '#5aa27c'
GREEN_BRIGHT = '#32B92D'
GREEN_DARK = '#249464'
GREEN_DARKER = '#146444'
BLUE = '#0072BB'
VIOLET = '#332288'
RED = '#eb0202'
REDISH = '#FF4C3B'
YELLOW = '#FFD034'
ORANGE = '#f79e02'

# strategies
LEFT = 'left'  # the left (or upper, or alpha) one, risk-dominant in the complex matrix
RIGHT = 'right'  # the right (or lower, or beta) one, payoff-dominant in the complex matrix

# update rules
UNCOND_IMITATION = 2
REPLICATOR = 3
BEST_RESPONSE = 4

# update rules short names dict
rules_names = {
    UNCOND_IMITATION: 'UI',
    REPLICATOR: 'RD',
    BEST_RESPONSE: 'BR',
}

# payoff matrix
COMPLEX = 0  # complex one with -b
SIMPLE = 1  # simple one with 1,1 and 0,0
GENERIC = 1000  # generic payoff matrix with all entries R, P, T, S to define

# loop type
ASYNC = 5  # one node at a time
SYNC = 6

