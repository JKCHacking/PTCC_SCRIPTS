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
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        position = holoplot_userdata.get_position(spec_name)
        self.assertEqual("STC01-500,00", position)

    def test_revision_02(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        revision = holoplot_userdata.get_revision()
        self.assertEqual("00", revision)

    def test_article_at_03(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        article_at = holoplot_userdata.get_article_at(spec_name)
        self.assertEqual("1421-STC01-500,00", article_at)

    def test_weight_polysurface_AL_12(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        group = holoplot_userdata.get_group(top_chord_id)
        weight = holoplot_userdata.get_weight(top_chord_id, group)
        expected_weight = round(0.0016657682 * 2710, 4)
        self.assertEqual(expected_weight, weight)

    def test_weight_polysurface_SS_12(self):
        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        group = holoplot_userdata.get_group(cp_id)
        weight = holoplot_userdata.get_weight(cp_id, group)
        self.assertEqual(1.2959, weight)

    def test_weight_block_12(self):
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        group = holoplot_userdata.get_group(non_std_truss_id)
        weight = holoplot_userdata.get_weight(non_std_truss_id, group)
        expected_weight = round(0.0081595586 * 2710, 4)
        self.assertEqual(round(expected_weight, 2), round(weight, 2))

    def test_screw_lock_15(self):
        screw_lock = holoplot_userdata.get_screw_lock()
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
        profession = holoplot_userdata.get_profession()
        self.assertEqual("HOL", profession)

    def test_delivery_53(self):
        pass

    def test_category_54(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        frame_pr_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]
        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        std_part_assm = rs.ObjectsByName("1421-H01-TSP-VP05")[0]

        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        category = holoplot_userdata.get_category(spec_name)
        self.assertEqual("Standard Parts Single", category)

        spec_name = holoplot_userdata.get_specific_part_name(frame_pr_id)
        category = holoplot_userdata.get_category(spec_name)
        self.assertEqual("Single Part", category)

        spec_name = holoplot_userdata.get_specific_part_name(non_std_truss_id)
        category = holoplot_userdata.get_category(spec_name)
        self.assertEqual("Pre-Assembly", category)

        spec_name = holoplot_userdata.get_specific_part_name(std_part_assm)
        category = holoplot_userdata.get_category(spec_name)
        self.assertEqual("Standard Parts Assembly", category)

    def test_assembly_55(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        assembly = holoplot_userdata.get_assembly(top_chord_id)
        self.assertEqual("H01", assembly)

    def test_template_at_04(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(top_chord_id)
        category = holoplot_userdata.get_category(spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2065", template_at)

        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(cp_id)
        category = holoplot_userdata.get_category(spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2106", template_at)

        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        spec_name = holoplot_userdata.get_specific_part_name(non_std_truss_id)
        group = holoplot_userdata.get_group(non_std_truss_id)
        category = holoplot_userdata.get_category(spec_name)
        template_at = holoplot_userdata.get_template_at(group, category)
        self.assertEqual("2152", template_at)

    def test_template_de(self):
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(top_chord_id)
        category = holoplot_userdata.get_category(spec_name)
        template_de = holoplot_userdata.get_template_de(group, category)
        self.assertEqual("V-AL09", template_de)

        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        spec_name = holoplot_userdata.get_specific_part_name(top_chord_id)
        group = holoplot_userdata.get_group(cp_id)
        category = holoplot_userdata.get_category(spec_name)
        template_de = holoplot_userdata.get_template_de(group, category)
        self.assertEqual("V-VA09", template_de)

        non_std_truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        spec_name = holoplot_userdata.get_specific_part_name(non_std_truss_id)
        group = holoplot_userdata.get_group(non_std_truss_id)
        category = holoplot_userdata.get_category(spec_name)
        template_de = holoplot_userdata.get_template_de(group, category)
        self.assertEqual("V-AL21", template_de)

        profile_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]
        spec_name = holoplot_userdata.get_specific_part_name(profile_id)
        group = holoplot_userdata.get_group(profile_id)
        category = holoplot_userdata.get_category(spec_name)
        template_de = holoplot_userdata.get_template_de(group, category)
        self.assertEqual("V-AL35", template_de)

    def test_name(self):
        std_part_single_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        std_part_assm_id = rs.ObjectsByName("1421-H01-TSP-VP05")[0]
        single_part_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]
        assm_id = rs.ObjectsByName("1421-H01-T03")[0]

        spec_name = holoplot_userdata.get_specific_part_name(std_part_single_id)
        category = holoplot_userdata.get_category(spec_name)
        name = holoplot_userdata.get_name(spec_name, category)
        self.assertEqual("1421-STC01-500,00 ... standard top chord", name)

        spec_name = holoplot_userdata.get_specific_part_name(std_part_assm_id)
        category = holoplot_userdata.get_category(spec_name)
        name = holoplot_userdata.get_name(spec_name, category)
        self.assertEqual("1421-H01-TSP-VP05 ... vertical part", name)

        spec_name = holoplot_userdata.get_specific_part_name(single_part_id)
        category = holoplot_userdata.get_category(spec_name)
        name = holoplot_userdata.get_name(spec_name, category)
        self.assertEqual("1421-H01-F01-PR01 ... profile", name)

        spec_name = holoplot_userdata.get_specific_part_name(assm_id)
        category = holoplot_userdata.get_category(spec_name)
        name = holoplot_userdata.get_name(spec_name, category)
        self.assertEqual("1421-H01-T03 ... truss assembly", name)

    def test_material(self):
        truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        top_chord_id = rs.ObjectsByName("1421-STC01-500,00")[0]
        vp_id = rs.ObjectsByName("1421-H01-TSP-VP05")[0]
        cp_id = rs.ObjectsByName("1421-H01-F01-CP01")[0]
        pr_id = rs.ObjectsByName("1421-H01-F01-PR01")[0]

        group = holoplot_userdata.get_group(truss_id)
        material = holoplot_userdata.get_material(group)
        self.assertEqual("aluminum EN AW-5754", material)

        group = holoplot_userdata.get_group(top_chord_id)
        material = holoplot_userdata.get_material(group)
        self.assertEqual("aluminum EN AW-5754", material)

        group = holoplot_userdata.get_group(vp_id)
        material = holoplot_userdata.get_material(group)
        self.assertEqual("aluminum EN AW-5754", material)

        group = holoplot_userdata.get_group(cp_id)
        material = holoplot_userdata.get_material(group)
        self.assertEqual("stainless steel 1.4571", material)

        group = holoplot_userdata.get_group(pr_id)
        material = holoplot_userdata.get_material(group)
        self.assertEqual("aluminum EN AW-6060 T66", material)

    def test_add_userdata(self):
        truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        holoplot_userdata.add_userdata(truss_id)
        self.assertEqual(rs.GetUserText(truss_id, "01_POSITION"), "H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "02_REVISION"), "00")
        self.assertEqual(rs.GetUserText(truss_id, "03_ARTICLE_AT"), "1421-H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "04_TEMPLATE_AT"), "2152")
        self.assertEqual(rs.GetUserText(truss_id, "05_ARTICLE_DE"), "1421-H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "06_TEMPLATE_DE"), "V-AL21")
        self.assertEqual(rs.GetUserText(truss_id, "07_TEMPLATE_NAME_DE"), "AL-Element")
        self.assertEqual(rs.GetUserText(truss_id, "08_RAWMAT_NO_DE"), "V-AL21")
        self.assertEqual(rs.GetUserText(truss_id, "09_RAWMAT_NAME_DE"), "AL-Element")
        self.assertEqual(rs.GetUserText(truss_id, "10_NAME"), "1421-H01-T03 ... truss assembly")
        self.assertEqual(rs.GetUserText(truss_id, "11_MATERIAL"), "aluminum EN AW-5754")
        self.assertEqual(str(round(float(rs.GetUserText(truss_id, "12_MASS")), 2)), str(round(0.0081595586 * 2710, 2)))
        self.assertEqual(rs.GetUserText(truss_id, "13_SURFACE"), " ")
        self.assertEqual(rs.GetUserText(truss_id, "14_COLOUR"), " ")
        self.assertEqual(rs.GetUserText(truss_id, "15_SCREW_LOCK"), "NO")
        self.assertTrue(len(rs.GetUserText(truss_id, "21_LENGTH")) > 0)
        self.assertTrue(len(rs.GetUserText(truss_id, "22_WIDTH")) > 0)
        self.assertTrue(len(rs.GetUserText(truss_id, "23_HEIGHT")) > 0)
        self.assertEqual(rs.GetUserText(truss_id, "31_COATING_AREA"), "1.6429")
        self.assertTrue(len(rs.GetUserText(truss_id, "32_GROSS_AREA")) > 0)
        self.assertEqual(rs.GetUserText(truss_id, "33_NET_AREA"), "1.6429")
        self.assertEqual(rs.GetUserText(truss_id, "51_GROUP"), "AL sheet")
        self.assertEqual(rs.GetUserText(truss_id, "52_PROFESSION"), "HOL")
        self.assertEqual(rs.GetUserText(truss_id, "53_DELIVERY"), "S")
        self.assertEqual(rs.GetUserText(truss_id, "54_CATEGORY"), "Pre-Assembly")
        self.assertEqual(rs.GetUserText(truss_id, "55_ASSEMBLY"), "H01")

    def test_main(self):
        holoplot_userdata.main()
        truss_id = rs.ObjectsByName("1421-H01-T03")[0]
        self.assertEqual(rs.GetUserText(truss_id, "01_POSITION"), "H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "02_REVISION"), "00")
        self.assertEqual(rs.GetUserText(truss_id, "03_ARTICLE_AT"), "1421-H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "04_TEMPLATE_AT"), "2152")
        self.assertEqual(rs.GetUserText(truss_id, "05_ARTICLE_DE"), "1421-H01-T03")
        self.assertEqual(rs.GetUserText(truss_id, "06_TEMPLATE_DE"), "V-AL21")
        self.assertEqual(rs.GetUserText(truss_id, "07_TEMPLATE_NAME_DE"), "AL-Element")
        self.assertEqual(rs.GetUserText(truss_id, "08_RAWMAT_NO_DE"), "V-AL21")
        self.assertEqual(rs.GetUserText(truss_id, "09_RAWMAT_NAME_DE"), "AL-Element")
        self.assertEqual(rs.GetUserText(truss_id, "10_NAME"), "1421-H01-T03 ... truss assembly")
        self.assertEqual(rs.GetUserText(truss_id, "11_MATERIAL"), "aluminum EN AW-5754")
        self.assertEqual(str(round(float(rs.GetUserText(truss_id, "12_MASS")), 2)), str(round(0.0081595586 * 2710, 2)))
        self.assertEqual(rs.GetUserText(truss_id, "13_SURFACE"), " ")
        self.assertEqual(rs.GetUserText(truss_id, "14_COLOUR"), " ")
        self.assertEqual(rs.GetUserText(truss_id, "15_SCREW_LOCK"), "NO")
        self.assertTrue(len(rs.GetUserText(truss_id, "21_LENGTH")) > 0)
        self.assertTrue(len(rs.GetUserText(truss_id, "22_WIDTH")) > 0)
        self.assertTrue(len(rs.GetUserText(truss_id, "23_HEIGHT")) > 0)
        self.assertEqual(rs.GetUserText(truss_id, "31_COATING_AREA"), "1.6429")
        self.assertTrue(len(rs.GetUserText(truss_id, "32_GROSS_AREA")) > 0)
        self.assertEqual(rs.GetUserText(truss_id, "33_NET_AREA"), "1.6429")
        self.assertEqual(rs.GetUserText(truss_id, "51_GROUP"), "AL sheet")
        self.assertEqual(rs.GetUserText(truss_id, "52_PROFESSION"), "HOL")
        self.assertEqual(rs.GetUserText(truss_id, "53_DELIVERY"), "S")
        self.assertEqual(rs.GetUserText(truss_id, "54_CATEGORY"), "Pre-Assembly")
        self.assertEqual(rs.GetUserText(truss_id, "55_ASSEMBLY"), "H01")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(HoloplotUserDataTest("test_spec_name"))
    suite.addTest(HoloplotUserDataTest('test_position_01'))
    suite.addTest(HoloplotUserDataTest('test_revision_02'))
    suite.addTest(HoloplotUserDataTest('test_article_at_03'))
    suite.addTest(HoloplotUserDataTest('test_weight_polysurface_AL_12'))
    suite.addTest(HoloplotUserDataTest('test_weight_polysurface_SS_12'))
    suite.addTest(HoloplotUserDataTest('test_screw_lock_15'))
    suite.addTest(HoloplotUserDataTest('test_coating_area_polysurface_31'))
    suite.addTest(HoloplotUserDataTest('test_dimensions_polysurface_21_22_23'))
    suite.addTest(HoloplotUserDataTest('test_group_51'))
    suite.addTest(HoloplotUserDataTest('test_category_54'))
    suite.addTest(HoloplotUserDataTest('test_assembly_55'))
    suite.addTest(HoloplotUserDataTest('test_template_at_04'))
    suite.addTest(HoloplotUserDataTest('test_template_de'))
    suite.addTest(HoloplotUserDataTest('test_name'))
    suite.addTest(HoloplotUserDataTest('test_material'))
    suite.addTest(HoloplotUserDataTest('test_weight_block_12'))
    suite.addTest(HoloplotUserDataTest('test_coating_area_block_31'))
    suite.addTest(HoloplotUserDataTest('test_add_userdata'))
    suite.addTest(HoloplotUserDataTest('test_main'))
    unittest.TextTestRunner(verbosity=2).run(suite)
