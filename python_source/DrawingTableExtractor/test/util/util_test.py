import unittest
import time
import os
import shutil
from pywinauto.application import Application
from src.util.util import Utilities
from src.util.constants import Constants


class UtilTest(unittest.TestCase):

    def test_get_handle_by_title(self):
        self.bc = Application(backend="win32").start("C:\\Program Files\\Bricsys\\BricsCAD V20 en_US\\bricscad.exe")
        time.sleep(0.5)
        self.handle = Utilities.get_handle_by_title("BricsCAD")
        for h in self.handle:
            self.assertTrue(h)
        self.bc.kill()
    
    def test_clean_up_file(self):
        # create files in a directory
        test_directory = Constants.TEST_DIR
        temp_dir = os.path.join(test_directory, "temp_dir")
        os.mkdir(temp_dir)
        file1 = os.path.join(Constants.TEST_DIR, "testdata", "testdata1.dwg")
        file2 = os.path.join(Constants.TEST_DIR, "testdata", "testdata2.pdf")

        shutil.copyfile(file1, os.path.join(temp_dir, "testdata1.dwg"))
        shutil.copyfile(file2, os.path.join(temp_dir, "testdata2.pdf"))
        
        Utilities.clean_up_file([".dwg", ".pdf"], temp_dir)
        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        
        os.removedirs(temp_dir)
