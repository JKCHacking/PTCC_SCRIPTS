import os
import unittest
from src.fea.pre_processor import PreProcessor
from src.util.constants import Constants


class PreProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pre_processor = PreProcessor()

    def test_create_geometry_single_profile(self):
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry_list = self.pre_processor.create_geometry(testdata_file_path)
        print(geometry_list)
        self.assertTrue(True)
