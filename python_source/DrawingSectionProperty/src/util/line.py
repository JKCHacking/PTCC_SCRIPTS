import itertools
import numpy as np
from src.util.constants import Constants


def slope(origin, target):
    if target[0] == origin[0]:
        return 0
    else:
        m = (target[1] - origin[1]) / (target[0] - origin[0])
        return m


def line_eqn(origin, target):
    x = origin[0]
    y = origin[1]

    c = y - (slope(origin, target) * x)
    m = slope(origin, target)
    return m, c


def get_y(x, slope, c):
    # y = mx + c
    y = (slope * x) + c
    return y


def get_x(y, slope, c):
    # x = (y-c)/m
    if slope == 0:
        c = 0   # vertical lines never intersect with y-axis
    if slope == 0:
        slope = 1   # Do NOT divide by zero
    x = (y - c) / slope
    return x


def get_points_bet_points(origin, target):
    step = 0.05
    coord_list = []
    m, c = line_eqn(origin, target)

    # Step along x-axis
    for i in np.arange(origin[0], target[0] + step, step):
        y = get_y(i, m, c)
        coord_list.append([round(i, Constants.ROUND_PRECISION), round(y, Constants.ROUND_PRECISION)])

    # Step along y-axis
    for i in np.arange(origin[1], target[1] + step, step):
        x = get_x(i, m, c)
        coord_list.append([round(x, Constants.ROUND_PRECISION), round(i, Constants.ROUND_PRECISION)])

    # return unique list
    return list(k for k, _ in itertools.groupby(sorted(coord_list)))
