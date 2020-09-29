import unittest
import subprocess
import os
from shutil import copyfile
from src.util.constants import Constants


class SectionPropertyReporterTest(unittest.TestCase):

    def test_script_01(self):
        file_input = "testdata001.dxf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)
        
        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)
        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, file_input)))
