import unittest
import sys
import os
sys.path.append("{}/../src".format(os.path.dirname(os.path.realpath(__file__))))
import parts_to_stp
import rhinoscriptsyntax as rs


class PartsToStpTest(unittest.TestCase):
    def test_bounding_box(self):
        top_chord_id = rs.ObjectsByName("1421-H01-F01-CP01")
        bb_points = parts_to_stp.get_bounding_box(top_chord_id)
        rs.AddPoints(bb_points)
        for bb_pt in bb_points:
            print(bb_pt)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PartsToStpTest("test_bounding_box"))
    unittest.TextTestRunner(verbosity=2).run(suite)
