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
    m = slope(origin, target)
    c = y - (m * x)

    return m, c


def get_y(x, slope, c):
    # y = mx + c
    y = (slope * x) + c
    return y


# def get_x(y, slope, c):
#     # x = (y-c)/m
#     if slope == 0:
#         c = 0   # vertical lines never intersect with y-axis
#         slope = 1   # Do NOT divide by zero
#     x = (y - c) / slope
#     return x


def get_points_from_line(origin, target):
    step = 0.005
    coord_list = []
    m, c = line_eqn(origin, target)

    if origin[0] == target[0]:  # vertical line
        x = origin[0]
        for y in np.arange(origin[1], target[1], step):
            coord_list.append([round(x, Constants.ROUND_PRECISION), round(y, Constants.ROUND_PRECISION)])
    elif origin[1] == target[1]:  # horizontal line
        y = origin[1]
        for x in np.arange(origin[0], target[0], step):
            coord_list.append([round(x, Constants.ROUND_PRECISION), round(y, Constants.ROUND_PRECISION)])
    else:  # diagonal line
        for x in np.arange(origin[0], target[0] + step, step):
            y = get_y(x, m, c)
            coord_list.append([round(x, Constants.ROUND_PRECISION), round(y, Constants.ROUND_PRECISION)])

    # return unique list
    return sorted(coord_list, key=lambda p: [p[0], p[1]])
