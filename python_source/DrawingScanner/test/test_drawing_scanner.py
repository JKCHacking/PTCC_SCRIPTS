#!/usr/bin/env python

import unittest
from src.constants import Constants
import os
import csv
from src.drawing_scanner import DrawingScanner


class TestDrawingScanner(unittest.TestCase):

    def test_search_block(self):
        expected = 198
        input_path = os.path.join(Constants.INPUT_DIR, 'input.dwg')

        ds = DrawingScanner()
        document = ds.open_file(input_path)
        ms = ds.get_modelspace(document)
        self.data_dict = ds.search_blocks(ms)

        sum = 0
        for key, value in self.data_dict.items():
            sum += value

        self.assertEqual(expected, sum)

    def test_write_csv(self):
        output_path = os.path.join(Constants.OUTPUT_DIR, 'output_test.csv')
        expected_rows = 84

        with open(output_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            row_count = sum(1 for row in reader)

        self.assertEqual(True, os.path.exists(output_path))
        self.assertEqual(expected_rows, row_count)
