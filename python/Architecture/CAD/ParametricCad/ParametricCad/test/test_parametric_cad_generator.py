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
    def test_get_part_names(self):
        template_path = os.path.join(TEST_PATH, "testdata", "U443-A36_test.dwg")
        part_names = parametric_cad_generator.get_part_names(template_path)
        self.assertEqual(["W756222-000",
                          "W754147-000",
                          "W756221-000",
                          "W751235-000",
                          "SRT1409-000",
                          "W752222-000",
                          "W753219-000",
                          "G537-000",
                          "G488-000",
                          "ISO001-000",
                          "W752375-000",
                          "W752374-000",
                          "G1-000",
                          "G2-000",
                          "P1-000"], part_names)

    def test_find_col_idx(self):
        b_cad = parametric_cad_generator.get_cad_application()
        template_path = os.path.join(TEST_PATH, "testdata", "U443-A36_test.dwg")
        doc = b_cad.Documents.Open(template_path)
        table = doc.HandleToObject("7334F")
        col_idx = parametric_cad_generator.find_col_idx(table, "PART NUMBER")
        self.assertEqual(2, col_idx)
        doc.Close(False)

    def test_find_row_idx(self):
        b_cad = parametric_cad_generator.get_cad_application()
        template_path = os.path.join(TEST_PATH, "testdata", "U443-A36_test.dwg")
        doc = b_cad.Documents.Open(template_path)
        table = doc.HandleToObject("7334F")
        row_idx = parametric_cad_generator.find_row_idx(table, 2, "G488-000")
        self.assertEqual(10, row_idx)
        doc.Close(False)

    def test_find_part_table(self):
        b_cad = parametric_cad_generator.get_cad_application()
        template_path = os.path.join(TEST_PATH, "testdata", "U443-A36_test.dwg")
        doc = b_cad.Documents.Open(template_path)
        table = parametric_cad_generator.find_part_table(doc)
        self.assertEqual(doc.HandleToObject("7334F"), table)
        doc.Close(False)

    def test_update_assembly_part_table(self):
        b_cad = parametric_cad_generator.get_cad_application()
        template_path = os.path.join(TEST_PATH, "testdata", "U443-A36_test.dwg")
        doc = b_cad.Documents.Open(template_path)
        parametric_cad_generator.update_assembly_part_table(doc, "W756222-024")
        part_table = doc.HandleToObject("7334F")
        self.assertEqual("W756222-024", part_table.GetCellValue(2, 2))
        doc.Close(False)

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

    def test_extract_variables(self):
        equation_string = "VAR1"
        self.assertEqual(["VAR1"], parametric_cad_generator.extract_variables(equation_string))
        equation_string = "VAR1 + VAR2"
        self.assertEqual(["VAR1", "VAR2"], parametric_cad_generator.extract_variables(equation_string))
        equation_string = "VAR + 2"
        self.assertEqual(["VAR"], parametric_cad_generator.extract_variables(equation_string))

    def test_equation_solver(self):
        equation_string = "VAR1 + VAR2"
        params = {"VAR1": "2", "VAR2": "3"}
        self.assertEqual("5", parametric_cad_generator.equation_resolver(equation_string, params))
