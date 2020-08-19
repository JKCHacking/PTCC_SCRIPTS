import unittest
import time
from pywinauto.application import Application
from src.util.util import Utilities


class UtilTest(unittest.TestCase):

    def test_get_handle_by_title(self):
        self.bc = Application(backend="win32").start("C:\\Program Files\\Bricsys\\BricsCAD V20 en_US\\bricscad.exe")
        time.sleep(0.5)
        self.handle = Utilities.get_handle_by_title("BricsCAD")
        for h in self.handle:
            self.assertTrue(h)
        self.bc.kill()
