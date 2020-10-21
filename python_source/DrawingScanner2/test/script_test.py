import os
import unittest
import csv
import shutil
from src.util.constants import Constants
from src.script import Script


class ScriptTest(unittest.TestCase):

    def test_iter_input_01(self):
        testdata_fname = 'testdata001.dxf'
        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)

        source = testdata_file
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)
        shutil.copyfile(source, dest)

        script = Script()
        script.iter_input()

        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)
        filename_ext = os.path.basename(testdata_file)
        filename = os.path.splitext(filename_ext)[0]
        expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)

        self.assertTrue(os.path.exists(expected_output_path))
        # delete the generated files in the output folder
        # os.remove(expected_output_path)
        # delete the copied files in the input folder
        os.remove(dest)

    def test_iter_input_02(self):
        testdata_fname = 'testdata002.dxf'
        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)

        source = testdata_file
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)
        shutil.copyfile(source, dest)

        script = Script()
        script.iter_input()

        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)
        filename_ext = os.path.basename(testdata_file)
        filename = os.path.splitext(filename_ext)[0]
        expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)

        self.assertTrue(os.path.exists(expected_output_path))
        # delete the generated files in the output folder
        # os.remove(expected_output_path)
        # delete the copied files in the input folder
        os.remove(dest)

    def test_iter_input_03(self):
        testdata_fname = 'testdata003.dxf'
        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)

        source = testdata_file
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)
        shutil.copyfile(source, dest)

        script = Script()
        script.iter_input()

        testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fname)
        filename_ext = os.path.basename(testdata_file)
        filename = os.path.splitext(filename_ext)[0]
        expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
        dest = os.path.join(Constants.INPUT_DIR, testdata_fname)

        self.assertTrue(os.path.exists(expected_output_path))
        # delete the generated files in the output folder
        # os.remove(expected_output_path)
        # delete the copied files in the input folder
        os.remove(dest)

    def test_iter_input_04(self):
        testdata_list = ['testdata001.dxf', 'testdata002.dxf', 'testdata003.dxf',
                         'testdata004.dxf', 'testdata005.dxf', 'testdata006.dxf']
        for testdata_fn in testdata_list:
            testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fn)
            source = testdata_file
            dest = os.path.join(Constants.INPUT_DIR, testdata_fn)
            shutil.copyfile(source, dest)

        script = Script()
        script.iter_input()

        for testdata_fn in testdata_list:
            testdata_file = os.path.join(Constants.TEST_DIR, "testdata", testdata_fn)
            filename_ext = os.path.basename(testdata_file)
            filename = os.path.splitext(filename_ext)[0]
            expected_output_path = os.path.join(Constants.OUTPUT_DIR, filename + '.xlsx')
            dest = os.path.join(Constants.INPUT_DIR, testdata_fn)

            self.assertTrue(os.path.exists(expected_output_path))
            # delete the generated files in the output folder
            # os.remove(expected_output_path)
            # delete the copied files in the input folder
            # os.remove(dest)
