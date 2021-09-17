# Test File: MODEL 3D Test.3dm
import sys
import os
sys.path.append("{}/../src".format(os.path.dirname(os.path.realpath(__file__))))
import holoplot_userdata
reload(holoplot_userdata)
import unittest
import rhinoscriptsyntax as rs
import scriptcontext as sc


class HoloplotUserDataTest(unittest.TestCase):
    def test_spec_name(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        self.assertEqual("1421-STC01-500,00", spec_name)

    def test_position_01(self):
        obj_ids = rs.ObjectsByName("1421-STC01-500,00")
        obj_id = obj_ids[0]
        position = holoplot_userdata.get_position(obj_id)
        self.assertEqual("STC01-500,00", position)

    def test_revision_02(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        revision = holoplot_userdata.get_revision(top_chord_id)
        self.assertEqual("00", revision)

    def test_article_at_03(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        article_at = holoplot_userdata.get_article_at(top_chord_id)
        self.assertEqual("1421-STC01-500,00", article_at)

    def test_article_de_05(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        article_de = holoplot_userdata.get_article_at(top_chord_id)
        self.assertEqual("1421-STC01-500,00", article_de)

    def test_weight_polysurface_AL_12(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        weight = holoplot_userdata.get_weight(top_chord_id)
        expected_weight = round(0.0016657682 * 2710, 4)
        self.assertEqual(expected_weight, weight)

    def test_weight_polysurface_SS_12(self):
        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        weight = holoplot_userdata.get_weight(cp_id)
        self.assertEqual(1.2959, weight)

    def test_weight_block_12(self):
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        weight = holoplot_userdata.get_weight(non_std_truss_id)
        expected_weight = round(0.0081595586 * 2710, 4)
        self.assertEqual(round(expected_weight, 2), round(weight, 2))

    def test_screw_lock_15(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        screw_lock = holoplot_userdata.get_screw_lock(top_chord_id)
        self.assertEqual("NO", screw_lock)

    def test_coating_area_polysurface_31(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        coating_area = holoplot_userdata.get_coating_area(top_chord_id)
        self.assertEqual(0.3231, coating_area)

    def test_coating_area_block_31(self):
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        coating_area = holoplot_userdata.get_coating_area(non_std_truss_id)
        self.assertEqual(1.6429, coating_area)

    def test_dimensions_polysurface_21_22_23(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        length, width, height = holoplot_userdata.get_dimensions(top_chord_id)
        self.assertEqual(3348.86, length)
        self.assertEqual(50.00, width)
        self.assertEqual(20.00, height)

    # def test_dimensions_block_21_22_23(self):
    #     obj_ids = self.get_object("blockinstance")
    #     obj_id = obj_ids[0]
    #     length, width, height = holoplot_userdata.get_dimensions(obj_id)
    #     self.assertAlmostEqual(4923.63, length, places=1)
    #     self.assertAlmostEqual(518.06, width, places=1)
    #     self.assertAlmostEqual(83.19, height, places=1)

    def test_group_51(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        frame_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]
        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]

        group = holoplot_userdata.get_group(top_chord_id)
        self.assertEqual("AL sheet", group)
        group = holoplot_userdata.get_group(non_std_truss_id)
        self.assertEqual("AL sheet", group)
        group = holoplot_userdata.get_group(frame_id)
        self.assertEqual("AL profile", group)
        group = holoplot_userdata.get_group(cp_id)
        self.assertEqual("SS sheet", group)

    def test_profession_52(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        profession = holoplot_userdata.get_profession(top_chord_id)
        self.assertEqual("HOL", profession)

    def test_delivery_53(self):
        pass

    def test_category_54(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        frame_pr_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        std_truss_id = rs.ObjectsByName("1421-ST01-500,00")[0]

        category = holoplot_userdata.get_category(top_chord_id)
        self.assertEqual("Standard Parts Single", category)
        category = holoplot_userdata.get_category(std_truss_id)
        self.assertEqual("Standard Parts Assembly", category)
        category = holoplot_userdata.get_category(frame_pr_id)
        self.assertEqual("Single Part", category)
        category = holoplot_userdata.get_category(non_std_truss_id)
        self.assertEqual("Pre-Assembly", category)

    def test_assembly_55(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        assembly = holoplot_userdata.get_assembly(top_chord_id)
        self.assertEqual("H01", assembly)

    def test_template_at_04(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(top_chord_id)
        category = holoplot_userdata.get_category(top_chord_id, spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2065", template_at)

        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(cp_id)
        category = holoplot_userdata.get_category(cp_id, spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2106", template_at)

        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        spec_name = holoplot_userdata.get_specific_part_name(non_std_truss_id)
        group = holoplot_userdata.get_group(non_std_truss_id)
        category = holoplot_userdata.get_category(non_std_truss_id, spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2152", template_at)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(HoloplotUserDataTest("test_spec_name"))
    # suite.addTest(HoloplotUserDataTest('test_position_01'))
    # suite.addTest(HoloplotUserDataTest('test_revision_02'))
    # suite.addTest(HoloplotUserDataTest('test_article_at_03'))
    # suite.addTest(HoloplotUserDataTest('test_article_de_05'))
    # suite.addTest(HoloplotUserDataTest('test_weight_polysurface_AL_12'))
    # suite.addTest(HoloplotUserDataTest('test_weight_polysurface_SS_12'))
    # suite.addTest(HoloplotUserDataTest('test_screw_lock_15'))
    # suite.addTest(HoloplotUserDataTest('test_coating_area_polysurface_31'))
    # suite.addTest(HoloplotUserDataTest('test_dimensions_polysurface_21_22_23'))
    # suite.addTest(HoloplotUserDataTest('test_group_51'))
    # suite.addTest(HoloplotUserDataTest('test_category_54'))
    # suite.addTest(HoloplotUserDataTest('test_assembly_55'))
    suite.addTest(HoloplotUserDataTest('test_template_at_04'))
    # this needs to be manually run because it modifies the test 3d document.
    # you have to undo the file manually using ctrl+Z
    # suite.addTest(HoloplotUserDataTest('test_weight_block_12'))
    # suite.addTest(HoloplotUserDataTest('test_coating_area_block_31'))
    unittest.TextTestRunner(verbosity=2).run(suite)
