import csv
import os
import unittest
from shutil import copyfile
from src.tower_measurer2 import Script
from src.constants import Constants
from src.tower_measurer2 import main


class TowerMeasurer2Test(unittest.TestCase):
    def tearDown(self) -> None:
        # remove all BAK files in the test directory.
        self.__remove_files(Constants.TESTDATA_DIR, Constants.BAK_FILES)
        self.__remove_files(Constants.TEST_DIR, Constants.CSV_FILES)
        # remove all unnecessary in input folder
        self.__remove_files(Constants.INPUT_DIR, Constants.DWG_FILES)
        self.__remove_files(Constants.INPUT_DIR, Constants.DXF_FILES)
        self.__remove_files(Constants.INPUT_DIR, Constants.BAK_FILES)
        # remove all unnecessary in output folder
        self.__remove_files(Constants.OUTPUT_DIR, Constants.CSV_FILES)

    def __remove_files(self, dir_name, file_extension):
        print("Removing unnecessary files...")
        for dir_path, dir_names, file_names in os.walk(dir_name):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(file_extension):
                    os.remove(file_full_path)

    def test_single_panel_surface(self):
        file_path = os.path.join(Constants.TESTDATA_DIR, "single_panel.dwg")
        script = Script()
        script.open_document(file_path)
        actual = script.get_total_area()
        actual = "{} {}**2".format(actual, script.get_unit_document())
        script.close_document()

        expected = "19875.8582 Millimeters**2"
        self.assertEqual(expected, actual)

    def test_single_panel_region(self):
        file_path = os.path.join(Constants.TESTDATA_DIR, "single_panel_region.dwg")
        script = Script()
        script.open_document(file_path)
        actual = script.get_total_area()
        actual = "{} {}**2".format(actual, script.get_unit_document())
        script.close_document()

        expected = "9261.1806 Millimeters**2"
        self.assertEqual(expected, actual)

    def test_5_panel_surface(self):
        file_path = os.path.join(Constants.TESTDATA_DIR, "5_panel.dwg")
        script = Script()
        script.open_document(file_path)
        actual = script.get_total_area()
        actual = "{} {}**2".format(actual, script.get_unit_document())
        script.close_document()

        expected = "96580.1716 Millimeters**2"
        self.assertEqual(expected, actual)

    def test_write_csv(self):
        script = Script()
        output_file = os.path.join(Constants.TEST_DIR, "output_test.csv")
        script.write_csv("sample1.dwg", 1234, output_file)
        script.write_csv("sample2.dwg", 4567, output_file)

        self.assertTrue(os.path.exists(output_file))

        expected_list = [["DWG File Name", "Total Surface Area"],
                         ["sample1.dwg", '1234'],
                         ["sample2.dwg", "4567"]]
        with open(output_file, mode="r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.assertTrue(row in expected_list)

    def test_main(self):
        output_file_path = os.path.join(Constants.OUTPUT_DIR, "output.csv")
        input_file_path = os.path.join(Constants.INPUT_DIR, "single_panel.dwg")
        file_test_path = os.path.join(Constants.TESTDATA_DIR, "single_panel.dwg")
        copyfile(file_test_path, input_file_path)
        main()
        self.assertTrue(os.path.exists(output_file_path))
        expected_list = [["DWG File Name", "Total Surface Area"],
                         ["single_panel.dwg", "19875.8582"]]

        with open(output_file_path, mode="r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.assertTrue(row in expected_list)
