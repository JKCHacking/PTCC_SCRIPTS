import os
import unittest
import sectionproperties.pre.sections as sections
from src.fea.pre_processor import PreProcessor
from src.util.constants import Constants


class PreProcessorTest(unittest.TestCase):

    # =============================CREATE_GEOMETRY_TEST==============================================
    def test_create_geometry_01(self):
        """
        Case #1:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        Expected: Will detect the 1 profile and the 1 hole
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

    def test_create_geometry_02(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        Expected: will detect the 1 profile and 2 holes
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

    def test_create_geometry_03(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        Expected: will detect the 1 profile and the 1 hole
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

    def test_create_geometry_04(self):
        """
        Case #1:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        Expected: will detect the 1 profile and the 5 hole
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

    def test_create_geometry_05(self):
        """
        Case #2:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Circle
        * Has hole: Yes
        Expected: PASS (will detect the 1 profile and the 2 hole)
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

    def test_create_geometry_06(self):
        """Case #3:
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Has hole: No
        Expected: PASS (it will detect the 1 profile and should have no holes)
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

    def test_create_geometry_07(self):
        """
        Case #3:
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Has hole: No
        Expected: PASS (it will detect the 1 profile and should have no holes)
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

    def test_create_geometry_08(self):  # LIMITATION
        """
        Case #4: - LIMITATION (it will not detect the profile and will Detect the holes as profiles)
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Non-Polyline (Lines and Arcs)
        * Profile1 Hole: None
        * Has hole: No
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

    def test_create_geometry_09(self):
        """
        Case #5: - will not detect the profile and will not detect the holes as profiles
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Non-Polyline (Lines and Arcs)
        * Profile1 Hole: Polyline
        * Has hole: Yes
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata008.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        self.assertEqual(None, geometry)

    def test_create_geometry_10(self):
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

    def test_create_geometry_11(self):
        """
        Desc: This should test in determining a hole when two profiles are in contact.
        * Complexity: Complex
        * Profile No: 2
        * Profile1: Polyline, 2 Polyline Hole
        * Profile2: Polyline, 1 Polyline Hole
        * Has hole: Yes

        The contact creates another hole between profiles. therefore there should be additional holes
        2(Profile 1) + 1 (Profile 2) + 1 (contact) = 4 holes
        """
        segment_size = 0.25
        has_holes = True
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata009.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        geometry1 = geometry_list[0]
        geometry2 = geometry_list[1]
        self.assertEqual(2, len(geometry_list))
        self.assertEqual(2, len(geometry1.holes))
        self.assertEqual(1, len(geometry2.holes))
        self.assertEqual(4, len(geometry.holes))
        geometry1.plot_geometry()
        geometry2.plot_geometry()
        geometry.plot_geometry()

    def test_create_geometry_12(self):
        """
        Case #7: - PASS (will only detect profile 1)
        * Complexity: Complex
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Type: Non-Polyline
        * Profile2 Hole: Polyline
        * Has hole: Yes
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

    def test_create_geometry_13(self):
        """
        * Complexity: Simple
        * Profile No: 3
        * Profile1: Polyline, No Hole
        * Profile2: Polyline, No Hole
        * Profile3: Polyline, No Hole
        * Has hole: No

        Warning: This test does not pass
        """
        segment_size = 0.25
        has_holes = False
        pre_processor = PreProcessor()

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata014.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        geometry_list = pre_processor.geometry_list
        geometry1 = geometry_list[0]
        geometry2 = geometry_list[1]
        geometry3 = geometry_list[2]
        self.assertEqual(2, len(geometry_list))
        self.assertEqual(2, len(geometry1.holes))
        self.assertEqual(1, len(geometry2.holes))
        self.assertEqual(2, len(geometry.holes))
        geometry1.plot_geometry()
        geometry2.plot_geometry()
        geometry3.plot_geometry()
        geometry.plot_geometry()

    # =============================CREATE_SECTION_TEST==============================================
    def test_create_section_01(self):
        '''
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata004.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_02(self):
        '''
        * Complexity: Complex
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_03(self):
        '''
        * Complexity: Simple
        * Profile No: 1
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata002.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_04(self):
        '''
        * Complexity: Simple
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Has hole: Yes
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata011.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_05(self):
        '''
        * Complexity: Complex
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: Polyline
        * Profile2 Type: Polyline
        * Profile2 Hole: Polyline
        * Has hole: Yes
        '''
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = True
        pre_processor = PreProcessor()
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata009.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_06(self):
        """
        * Complexity: Simple
        * Profile No: 2
        * Profile1 Type: Polyline
        * Profile1 Hole: None
        * Profile2 Type: Polyline
        * Profile2 Hole: None
        * Has hole: False
        """
        pre_processor = PreProcessor()
        materials = None

        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])

        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        cross_section = pre_processor.create_section([isection, box], mesh, materials)
        cross_section.plot_mesh()

    def test_create_section_07(self):
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

    def test_create_section_08(self):
        """
            * Complexity: Simple
            * Profile No: 3
            * Profile1: Polyline, No hole
            * Profile2: Polyline, No hole
            * Profile3: Polyline, No hole
            * Has hole: False
            * Has Material: False
        """
        pre_processor = PreProcessor()
        segment_size = 0.25
        mesh_size = 5.0
        has_holes = False
        materials = None

        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata014.dxf")
        geometry = pre_processor.create_geometry(testdata_file_path, has_holes, segment_size)
        mesh = pre_processor.create_mesh(geometry, mesh_size)
        cross_section = pre_processor.create_section(geometry, mesh, materials)
        cross_section.plot_mesh()

    # ============================================== CREATE MATERIAL TEST ==============================
    def test_create_material_01(self):
        """
        Desc: no materials will be implemented on the profiles
        material = 0
        profile = 2
        """

        error_list = []
        materials = None
        pre_proc = PreProcessor()

        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])
        pre_proc.geometry_list = [isection, box]

        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        try:
            cross_section = pre_proc.create_section([isection, box], mesh, materials)
            cross_section.plot_mesh(materials=True)
        except AssertionError as ae:
            print(str(ae))
            error_list.append(ae)
        self.assertEqual(0, len(error_list))

    def test_create_material_02(self):
        """
        Desc: material 1 will be used on the both profiles
        material = 1
        profile = 2
        """
        materials = ["aluminum_ams_nmms"]
        error_list = []

        pre_proc = PreProcessor()
        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])

        pre_proc.geometry_list = [isection, box]
        material_list = pre_proc.create_materials(materials)
        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        try:
            cross_section = pre_proc.create_section([isection, box], mesh, material_list)
            cross_section.plot_mesh(materials=True)
        except AssertionError as ae:
            print(str(ae))
            error_list.append(ae)

        self.assertEqual(0, len(error_list))

    def test_create_material_03(self):
        """
        Desc: material 1 to profile 1, material 2 to profile 2
        material = 2
        profile = 2
        """
        materials = ["aluminum_ams_nmms", "carbon_steel_ams_nmms"]
        error_list = []

        pre_proc = PreProcessor()
        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])

        pre_proc.geometry_list = [isection, box]
        material_list = pre_proc.create_materials(materials)

        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        try:
            cross_section = pre_proc.create_section([isection, box], mesh, material_list)
            cross_section.plot_mesh(materials=True)
        except AssertionError as ae:
            print(str(ae))
            error_list.append(ae)

        self.assertEqual(0, len(error_list))

    def test_create_material_04(self):
        """
        Desc: material 1 to profile 1, material 2 to profile 2, material 2 to profile 3.
        material = 2
        profile = 3
        """
        materials = ["aluminum_ams_nmms", "carbon_steel_ams_nmms"]
        error_list = []

        pre_proc = PreProcessor()
        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])
        octagon = sections.PolygonSection(d=200, t=6, n_sides=8, r_in=20, n_r=12)
        pre_proc.geometry_list = [isection, box, octagon]
        geometry = sections.MergedSection([isection, box, octagon])
        mesh = geometry.create_mesh([1.5, 2.0, 2.5])
        material_list = pre_proc.create_materials(materials)
        try:
            cross_section = pre_proc.create_section([isection, box, octagon], mesh, material_list)
            cross_section.plot_mesh(materials=True)
        except AssertionError as ae:
            print(str(ae))
            error_list.append(ae)

        self.assertEqual(0, len(error_list))

    def test_create_material_05(self):
        """
        Desc: material 1 to profile 1, material 2 to profile 2, material 3 will be disregarded.
        material = 3
        profile = 2
        """
        materials = ["aluminum_ams_nmms", "carbon_steel_ams_nmms", "stainless_steel_ams_nmms"]
        error_list = []

        pre_proc = PreProcessor()
        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])
        pre_proc.geometry_list = [isection, box]
        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        material_list = pre_proc.create_materials(materials)

        try:
            cross_section = pre_proc.create_section([isection, box], mesh, material_list)
            cross_section.plot_mesh(materials=True)
        except AssertionError as ae:
            print(str(ae))
            error_list.append(ae)

        self.assertEqual(0, len(error_list))


if __name__ == "__main__":
    unittest.main()
