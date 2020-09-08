import os
import unittest
import ezdxf
from ezdxf.math import BoundingBox2d
from src.fea.pre_processor import PreProcessor
from src.util.constants import Constants


class PreProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        segment_size = 0.25
        self.pre_processor = PreProcessor(segment_size)

    def test_create_geometry_single_profile(self):
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry_list = self.pre_processor.create_geometry(testdata_file_path)
        self.assertTrue(True)

    def test_create_simple_single_geometry(self):
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata004.dxf")
        geometry_list = self.pre_processor.create_geometry(testdata_file_path)

        self.assertEquals(1, len(geometry_list))

    def test_calc_arc_segmentation(self):
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata003.dxf")
        dxf_doc = ezdxf.readfile(testdata_file_path)
        arc_ent = dxf_doc.entitydb["CB"]
        s_pt = list(arc_ent.start_point)[:-1]
        e_pt = list(arc_ent.end_point)[:-1]
        shape_size = 0.5
        arc_seg_points = self.pre_processor.calculate_arc_segmentation(arc_ent, shape_size)
        res_len = len(arc_seg_points)
        self.assertEqual(630, res_len)
        self.assertAlmostEqual(s_pt[0], arc_seg_points[0][0])
        self.assertAlmostEqual(s_pt[1], arc_seg_points[0][1])
        self.assertAlmostEqual(e_pt[0], arc_seg_points[res_len - 1][0])
        self.assertAlmostEqual(e_pt[1], arc_seg_points[res_len - 1][1])
