import os
import unittest
from src.tower_measurer2 import Script
from src.constants import Constants


class TowerMeasurer2Test(unittest.TestCase):
    def test_single_panel_surface(self):
        file_path = os.path.join(Constants.TEST_DIR, "single_panel.dwg")
        script = Script()
        script.open_document(file_path)
        actual = script.get_total_area()
        actual = "{} {}**2".format(actual, script.get_unit_document())
        script.close_document()

        expected = "19875.8582 Millimeters**2"
        self.assertEqual(expected, actual)

    def test_5_panel_surface(self):
        file_path = os.path.join(Constants.TEST_DIR, "5_panel.dwg")
        script = Script()
        script.open_document(file_path)
        actual = script.get_total_area()
        actual = "{} {}**2".format(actual, script.get_unit_document())
        script.close_document()

        expected = "96580.1716 Millimeters**2"
        self.assertEqual(expected, actual)
