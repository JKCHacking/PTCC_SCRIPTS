import os
import unittest
from src.fea.pre_processor import PreProcessor
from src.util.constants import Constants


class PreProcessorTest(unittest.TestCase):

    def test_create_geometry_case_1_simple(self):
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor(segment_size, has_holes)

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata004.dxf")
        geometry_list = pre_processor.create_geometry(testdata_file_path)
        geometry = geometry_list[0]
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(1, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_1_complex(self):
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor(segment_size, has_holes)

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry_list = pre_processor.create_geometry(testdata_file_path)
        geometry = geometry_list[0]
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(2, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_2(self):
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor(segment_size, has_holes)

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata005.dxf")
        geometry_list = pre_processor.create_geometry(testdata_file_path)
        geometry = geometry_list[0]
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(2, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_3(self):
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor(segment_size, has_holes)

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata006.dxf")
        geometry_list = pre_processor.create_geometry(testdata_file_path)
        geometry = geometry_list[0]
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(0, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_3_complex(self):
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor(segment_size, has_holes)

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata007.dxf")
        geometry_list = pre_processor.create_geometry(testdata_file_path)
        geometry = geometry_list[0]
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(0, len(geometry.holes))
        geometry.plot_geometry()
