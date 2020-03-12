#!/usr/bin/env python

from math import tan
from math import degrees
from math import sqrt
from math import acos

MAX_OPENING = 354.0
TOP_TO_PIVOTAL = 92.0


class PayPayGenerator:
    def __init__(self, tile_length):
        self.tile_length = tile_length
        pass

    def calculate_divided_angle(self):
        opposite = MAX_OPENING - TOP_TO_PIVOTAL
        hypotenuse = self.tile_length
        adjacent = round(sqrt((hypotenuse ** 2) - (opposite ** 2)), 1)

        angle = round(degrees(acos((adjacent**2 + hypotenuse**2 - opposite**2)/(2.0 * adjacent * hypotenuse))), 2)
        divided_angle = round(angle / 8.00, 2)

        return divided_angle


if __name__ == "__main__":
    tile_len = 1423.0
    pp_gen = PayPayGenerator(tile_len)
    div_angle = pp_gen.calculate_divided_angle()
