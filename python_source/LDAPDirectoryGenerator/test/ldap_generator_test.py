import unittest
import os
import shutil
from src.util.constants import Constants
from src.ldp_generator import LDAPGenerator


class LdapGeneratorTest(unittest.TestCase):
    def clear_dir(self, dir, ext):
        for dir_path, dir_names, file_names in os.walk(dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(ext):
                    os.remove(file_full_path)

    def copy_testdata(self, testdata_name):
        testdata_fp = os.path.join(Constants.TEST_DIR, "testdata", testdata_name)
        src = testdata_fp
        dst = os.path.join(Constants.INPUT_DIR, testdata_name)
        shutil.copyfile(src, dst)

    def test_iter_input_001(self):
        '''Complete attribtues'''
        testdata = "testdata001.csv"
        test_result_file = os.path.join(Constants.OUTPUT_DIR, testdata.split(".")[0] + ".xlsx")
        self.copy_testdata(testdata)
        script = LDAPGenerator()
        script.iter_input()
        self.assertTrue(os.path.exists(test_result_file))
        self.clear_dir(Constants.INPUT_DIR, Constants.CSV_FILE_EXT)

    def test_iter_input_002(self):
        '''Missing attribute'''
        testdata = "testdata002.csv"
        test_result_file = os.path.join(Constants.OUTPUT_DIR, testdata.split(".")[0] + ".xlsx")
        self.copy_testdata(testdata)
        script = LDAPGenerator()
        script.iter_input()
        self.assertTrue(os.path.exists(test_result_file))
        self.clear_dir(Constants.INPUT_DIR, Constants.CSV_FILE_EXT)

    def test_iter_input_003(self):
        '''No attribute'''
        testdata = "testdata003.csv"
        test_result_file = os.path.join(Constants.OUTPUT_DIR, testdata.split(".")[0] + ".xlsx")
        self.copy_testdata(testdata)
        script = LDAPGenerator()
        script.iter_input()
        self.assertTrue(os.path.exists(test_result_file))
        self.clear_dir(Constants.INPUT_DIR, Constants.CSV_FILE_EXT)

    def test_iter_input_004(self):
        '''Multiple attribute, Alphabetical Order'''
        testdata = "testdata004.csv"
        test_result_file = os.path.join(Constants.OUTPUT_DIR, testdata.split(".")[0] + ".xlsx")
        self.copy_testdata(testdata)
        script = LDAPGenerator()
        script.iter_input()
        self.assertTrue(os.path.exists(test_result_file))
        self.clear_dir(Constants.INPUT_DIR, Constants.CSV_FILE_EXT)

    def test_iter_input_005(self):
        '''More than 40 row in each column in 1 sheet'''
        testdata = "testdata005.csv"
        test_result_file = os.path.join(Constants.OUTPUT_DIR, testdata.split(".")[0] + Constants.DOCX_FILE_EXT)
        self.copy_testdata(testdata)
        script = LDAPGenerator()
        script.iter_input()
        self.assertTrue(os.path.exists(test_result_file))
        self.clear_dir(Constants.INPUT_DIR, Constants.CSV_FILE_EXT)
