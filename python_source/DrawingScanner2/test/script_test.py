import os
import unittest
import csv
import shutil
from src.util.constants import Constants
from src.script import Script


class ScriptTest(unittest.TestCase):

    def test_iter_input_01(self):
        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", 'testdata001.dxf')
        source = testdata_file
        dest = os.path.join(Constants.INPUT_DIR, 'testdata001.dxf')
        shutil.copyfile(source, dest)

        script = Script()
        script.iter_input()

        filename_ext = os.path.basename(testdata_file)
        filename = os.path.splitext(filename_ext)[0]
        expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.csv')
        self.assertTrue(os.path.exists(expected_output_path))

        # there should be 3 rows
        expected_value_rows = [['7A', '4.2', '5'],
                               ['7C', '4.1', '1.8'],
                               ['7E', '3.9', '1.8']]

        with open(expected_output_path, newline='') as csvfile:
            # comparing the width and height of each polyline
            reader = csv.DictReader(csvfile)
            row_count = 0
            for row in reader:
                expected_handle = expected_value_rows[row_count][0]
                expected_width = float(expected_value_rows[row_count][1])
                expected_height = float(expected_value_rows[row_count][2])
                self.assertEqual(row['handle'], expected_handle)
                self.assertAlmostEqual(float(row['width']), expected_width)
                self.assertAlmostEqual(float(row['height']), expected_height)
                row_count += 1
            self.assertEqual(len(expected_value_rows), row_count)
        os.remove(expected_output_path)
        os.remove(dest)

    def test_create_output_01(self):
        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", 'testdata001.dxf')
        script = Script()
        script.create_output(testdata_file)

        # filename_ext = os.path.basename(testdata_file)
        # filename = os.path.splitext(filename_ext)[0]
        # expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.csv')
        # self.assertTrue(os.path.exists(expected_output_path))
        #
        # # there should be 3 rows
        # expected_value_rows = [['7A', '4.2', '5'],
        #                        ['7C', '4.1', '1.8'],
        #                        ['7E', '3.9', '1.8']]
        #
        # with open(expected_output_path, newline='') as csvfile:
        #     # comparing the width and height of each polyline
        #     reader = csv.DictReader(csvfile)
        #     row_count = 0
        #     for row in reader:
        #         expected_handle = expected_value_rows[row_count][0]
        #         expected_width = float(expected_value_rows[row_count][1])
        #         expected_height = float(expected_value_rows[row_count][2])
        #         self.assertEqual(row['handle'], expected_handle)
        #         self.assertAlmostEqual(float(row['width']), expected_width)
        #         self.assertAlmostEqual(float(row['height']), expected_height)
        #         row_count += 1
        #     self.assertEqual(len(expected_value_rows), row_count)
        # os.remove(expected_output_path)
