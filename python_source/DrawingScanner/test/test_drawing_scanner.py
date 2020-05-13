#!/usr/bin/env python

import unittest
from src.constants import Constants
import os
from src.drawing_scanner import DrawingScanner


class TestDrawingScanner(unittest.TestCase):

    def test_search_block(self):
        expected = 198
        input_path = os.path.join(Constants.INPUT_DIR, 'input.dwg')
        output_path = os.path.join(Constants.OUTPUT_DIR, 'output.csv')

        ds = DrawingScanner()
        document = ds.open_file(input_path)
        ms = ds.get_modelspace(document)
        data_dict = ds.search_blocks(ms)

        sum = 0
        for data in data_dict.items():
            sum += data[]