import os
import unittest
import sectionproperties.pre.sections as sections
from src.fea.pre_processor import PreProcessor
from src.util.constants import Constants


class PreProcessorTest(unittest.TestCase):

    # =============================CREATE_GEOMETRY_TEST==============================================
    def test_create_geometry_case_1_simple(self):
        """
        Case #1:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return: will detect the profile and the hole
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata004.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(1, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_1_complex(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return: will detect the profile and the hole
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(2, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_1_complex_2(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return: will detect the profile and the hole
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata002.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(1, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_1_complex_3(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return: will detect the profile and the hole
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata012.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(5, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_2(self):
        """
        Case #2:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Circle
        * Has hole: Yes
        :return: PASS (will detect the profile and the hole)
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata005.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(2, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_3(self):
        """Case #3:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Has hole: No
        :return: PASS (it will detect the profile and should have no holes)
        """
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata006.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(0, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_3_complex(self):
        """
        Case #3:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Has hole: No
        :return: PASS (it will detect the profile and should have no holes)
        """
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata007.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(0, len(geometry.holes))
        geometry.plot_geometry()

    def test_create_geometry_case_4_complex(self):  # LIMITATION
        """
        Case #4: - LIMITATION (it will not detect the profile and will Detect the holes as profiles)
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Non-Polyline (Lines and Arcs)
        * Profile1 Hole: None
        * Has hole: No
        :return:
        """
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata008.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        geometry1 = geometry_list[0]
        geometry2 = geometry_list[1]
        self.assertEqual(2, len(geometry_list))
        self.assertEqual(0, len(geometry1.holes))
        self.assertEqual(0, len(geometry2.holes))
        self.assertEqual(0, len(geometry.holes))
        geometry1.plot_geometry()
        geometry2.plot_geometry()
        geometry.plot_geometry()

    def test_create_geometry_case_5_complex(self):
        """
        Case #5: - will not detect the profile and will not detect the holes as profiles
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Non-Polyline (Lines and Arcs)
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata008.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        self.assertEqual(None, geometry)

    def test_create_geometry_2_simp_prof(self):
        """
        * Complexity: Simple
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile2 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Hole: Circle
        * Has hole: Yes
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata011.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        geometry1 = geometry_list[0]
        geometry2 = geometry_list[1]
        self.assertEqual(2, len(geometry_list))
        self.assertEqual(1, len(geometry1.holes))
        self.assertEqual(1, len(geometry2.holes))
        self.assertEqual(2, len(geometry.holes))
        geometry1.plot_geometry()
        geometry2.plot_geometry()
        geometry.plot_geometry()

    def test_create_geometry_case_6(self):
        """
        Case #6: - PASS (will detect 2 profiles with holes)
        * Complexity: Complex
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Type: Polyline
        * Profile2 Hole: Polyline
        * Has hole: Yes
        :return:
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata009.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        geometry1 = geometry_list[0]
        geometry2 = geometry_list[1]
        # self.assertEqual(2, len(geometry_list))
        # self.assertEqual(2, len(geometry1.holes))
        # self.assertEqual(1, len(geometry2.holes))
        # self.assertEqual(3, len(geometry.holes))
        geometry1.plot_geometry()
        geometry2.plot_geometry()
        geometry.plot_geometry()

    def test_create_geometry_case_7(self):
        """
        Case #7: - PASS (will only detect profile 1)
        * Complexity: Complex
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Type: Non-Polyline
        * Profile2 Hole: Polyline
        * Has hole: Yes
        :return
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata010.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        self.assertEqual(1, len(geometry_list))
        self.assertEqual(2, len(geometry.holes))
        geometry.plot_geometry()

    # =============================CREATE_SECTION_TEST==============================================
    def test_create_section_single_simple_profile(self):
        '''
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return:
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata004.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh)
        cross_section.plot_mesh()

    def test_create_section_single_complex_profile(self):
        '''
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return:
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh)
        cross_section.plot_mesh()

    def test_create_section_single_complex_profile_2(self):
        '''
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return:
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata002.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh)
        cross_section.plot_mesh()

    def test_create_section_2_simple_profile(self):
        '''
        * Complexity: Simple
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        :return:
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata011.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh)
        cross_section.plot_mesh()

    def test_create_section_2_complex_profile(self):
        '''
        * Complexity: Complex
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Type: Polyline
        * Profile2 Hole: Polyline
        * Has hole: Yes
        :return:
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata009.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh)
        cross_section.plot_mesh()

    def test_create_section_2_simple_profile_2(self):
        """
        * Complexity: Simple
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Profile2 Type: Polyline
        * Profile2 Hole: None
        * Has hole: False
        :return:
        """
        pre_processor = PreProcessor()

        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])

        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        cross_section = pre_processor.create_section([isection, box], mesh)
        cross_section.plot_mesh()

    def test_create_section_2_simple_profile_w_materials(self):
        """
            * Complexity: Simple
            * Profile No: 2
            * Profile1 Type: Polyline
            * Profile1 Hole: Polyline
            * Profile2 Type: Polyline
            * Profile2 Hole: Polyline
            * Has hole: Yes
            * Has Material: Yes
        """
        pre_processor = PreProcessor()
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        materials = ["aluminum_ams_nmms", "carbon_steel_ams_nmms"]

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata011.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        material_list = pre_processor.create_materials(materials)
        cross_section = pre_processor.create_section(geometry, mesh, material_list)
        cross_section.plot_mesh(materials=True)


if __name__ == "__main__":
    unittest.main()
