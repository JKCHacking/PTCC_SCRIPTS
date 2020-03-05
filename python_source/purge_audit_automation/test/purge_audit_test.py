#!usr/bin/env python

import unittest
import os
import sys
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
from subprocess import call
from purge_audit_script import PurgeAuditScript

PYTHON_EXE = sys.executable
APPLICATION_FILE_NAME = "purge_audit_script.py"


# MAJOR DIRECTORIES
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SRC_DIRECTORY = os.path.join(os.path.dirname(TEST_DIRECTORY), "src")
INPUT_DIRECTORY = os.path.join(os.path.dirname(TEST_DIRECTORY), "input")
OUTPUT_DIRECTORY = os.path.join(os.path.dirname(TEST_DIRECTORY), "output")
SCRIPT_PATH = os.path.join(SRC_DIRECTORY, APPLICATION_FILE_NAME)


class PurgeAuditTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_data_directory = os.path.join(TEST_DIRECTORY, "testdata")

    def tearDown(self) -> None:
        # empties input and output folder
        self.__empty_directory(INPUT_DIRECTORY)
        self.__empty_directory(OUTPUT_DIRECTORY)

    def __insert_test_data(self, file_name):
        print(f"Inserting {file_name} to input...")
        # copies specific content (directory or file) from test_data folder to input folder.
        source_path = os.path.join(self.test_data_directory, file_name)
        dest_path = INPUT_DIRECTORY
        if os.path.exists(source_path):
            if os.path.isdir(source_path):
                try:
                    copytree(source_path, dest_path)
                except FileExistsError:
                    print("Directory Exists Error!")
            elif os.path.isfile(source_path):
                try:
                    copyfile(source_path, dest_path)
                except FileExistsError:
                    print("File Exists Error")
        else:
            print(f"Specified path {source_path} does not exists!")

    @staticmethod
    def __empty_directory(directory):
        print(f"Cleaning up input and output folders...")
        # deletes all the contents of a specified directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except FileNotFoundError:
                print(f"File not Found {file_path}")

    @staticmethod
    def __run_script():
        call([PYTHON_EXE, SCRIPT_PATH])

    def test_1_file(self):
        print("==================test_1_file START============================")
        file_name = "CS-0001.dwg"
        self.__insert_test_data(file_name)
        self.__run_script()

        output_full_path = os.path.join(OUTPUT_DIRECTORY, file_name)
        self.assertTrue(os.path.exists(output_full_path))
        print("==================test_1_file END============================")

    def test_multiple_file(self):
        print("==================test_multiple_file START============================")
        file_name = "DWG"
        self.__insert_test_data(file_name)
        self.__run_script()

        output_full_path = os.path.join(OUTPUT_DIRECTORY, file_name)
        self.assertTrue(os.path.exists(output_full_path))
        print("==================test_multiple_file END============================")


if __name__ == "__main__":
    unittest.main()
