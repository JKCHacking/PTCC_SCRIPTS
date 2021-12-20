import os
import unittest
import shutil
from src import parametric_cad_generator


TEST_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(TEST_PATH)
PROJ_PATH = os.path.dirname(APP_PATH)
OUTPUT_PATH = os.path.join(PROJ_PATH, "output")
SRC_PATH = os.path.join(APP_PATH, "src")


class TestParametricCadGenerator(unittest.TestCase):
    def test_create_assembly(self):
        testdata = os.path.join(TEST_PATH, "testdata", "assembly_test.dwg")
        test_dir = os.path.join(OUTPUT_PATH, "test_asm")
        test_assembly = parametric_cad_generator.create_assembly(testdata, "test_asm", test_dir)
        self.assertTrue(os.path.exists(test_assembly.Path))
        test_assembly_path = test_assembly.Path
        test_assembly.Close(False)
        shutil.rmtree(test_assembly_path)

    def test_update_assembly_params(self):
        testdata = os.path.join(TEST_PATH, "testdata", "assembly_test.dwg")
        b_app = parametric_cad_generator.get_cad_application()
        test_doc = b_app.Documents.Open(testdata)
        params = {"MH": "100"}
        parametric_cad_generator.update_assembly_params(test_doc, params)
        # check if updated
        for obj in test_doc.ModelSpace:
            if obj.Layer in "*ADSK_CONSTRAINTS":
                self.assertEqual("100", obj.TextOverride.split("=")[1])
        test_doc.Close(False)

    def test_update_part_params(self):
        testdata = os.path.join(TEST_PATH, "testdata", "part_test.dwg")
        b_app = parametric_cad_generator.get_cad_application()
        test_doc = b_app.Documents.Open(testdata)
        asm_params = {"MH": "100"}
        parametric_cad_generator.update_part_params(test_doc, asm_params)
        self.assertEqual("100", test_doc.HandleToObject("7A").TextOverride)
        test_doc.Close(False)

    def test_get_all_assm_params(self):
        testdata = os.path.join(TEST_PATH, "testdata", "assembly_test.dwg")
        b_app = parametric_cad_generator.get_cad_application()
        test_doc = b_app.Documents.Open(testdata)
        self.assertEqual({"MH": "5.7"}, parametric_cad_generator.get_all_assm_params(test_doc))
        test_doc.Close(False)

    def test_get_all_part_params(self):
        testdata = os.path.join(TEST_PATH, "testdata", "part_test.dwg")
        b_app = parametric_cad_generator.get_cad_application()
        test_doc = b_app.Documents.Open(testdata)
        self.assertEqual({"MH": "5.7"}, parametric_cad_generator.get_all_part_params(test_doc))
        test_doc.Close(False)

    def test_find_duplicate_part(self):
        part_test = os.path.join(TEST_PATH, "testdata", "part_test.dwg")
        assembly_test = os.path.join(TEST_PATH, "testdata", "assembly_test.dwg")
        dest_dir = os.path.join(OUTPUT_PATH, "assembly_test")
        os.mkdir(dest_dir)
        shutil.copyfile(assembly_test, os.path.join(dest_dir, "assembly_test.dwg"))
        shutil.copyfile(part_test, os.path.join(dest_dir, "part_test.dwg"))

        # has duplicate
        duplicate, count = parametric_cad_generator.find_duplicate_part("part_test", {"MH": "5.7"})
        self.assertIsNotNone(duplicate)
        self.assertEqual(1, count)

        # no duplicate
        duplicate, count = parametric_cad_generator.find_duplicate_part("part_test", {"MH": "4.8"})
        self.assertIsNone(duplicate)
        self.assertEqual(1, count)
        shutil.rmtree(dest_dir)
