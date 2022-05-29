import unittest
import sys
import os
sys.path.append("{}/../src".format(os.path.dirname(os.path.realpath(__file__))))
import parts_to_stp
reload(parts_to_stp)
import rhinoscriptsyntax as rs


class PartsToStpTest(unittest.TestCase):
    def test_get_lying_plane(self):
        part_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        text_id = rs.ObjectsByName("TextTest1")[0]
        parts_to_stp.orient_to_top(part_id, text_id)

        part_id = rs.ObjectsByName("PartTest2")[0]
        text_id = rs.ObjectsByName("TextTest2")[0]
        parts_to_stp.orient_to_top(part_id, text_id)

    def test_search_pair_text(self):
        obj_id = rs.ObjectsByName("PartTest1")[0]
        txt_id = parts_to_stp.search_nearest_text(obj_id)
        rs.SelectObject(txt_id)
        self.assertEqual(rs.ObjectsByName("TextTest1")[0], txt_id)

        obj_id = rs.ObjectsByName("PartTest2")[0]
        txt_id = parts_to_stp.search_nearest_text(obj_id)
        rs.SelectObject(txt_id)
        self.assertEqual(rs.ObjectsByName("TextTest2")[0], txt_id)

    def test_export_to_stp(self):
        test_filename = "test_stp.stp"
        part_id = rs.ObjectsByName("PartTest3")[0]
        text_id = rs.ObjectsByName("TextTest3")[0]
        curve_ids = rs.ExplodeText(text_id)
        objs_to_export = [curve_id for curve_id in curve_ids]
        objs_to_export.append(part_id)
        parts_to_stp.export_to_stp(test_filename, objs_to_export)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(PartsToStpTest("test_get_lying_plane"))
    # suite.addTest(PartsToStpTest("test_search_pair_text"))
    suite.addTest(PartsToStpTest("test_export_to_stp"))
    unittest.TextTestRunner(verbosity=2).run(suite)
