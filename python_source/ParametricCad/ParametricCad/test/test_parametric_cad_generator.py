import os
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "src"))
from src.parametric_cad_generator import get_part_names,\
    get_cad_application, find_col_idx, find_row_idx, find_part_table, Assembly, Part


class ParametricCadGeneratorTest(unittest.TestCase):
    def test_get_subcomp_names(self):
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36_test.dwg"
        subcomp_names = get_part_names(template_path)
        self.assertEqual(["W756222 - 000",
                          "W754147 - 000",
                          "W756221 - 000",
                          "W751235 - 000",
                          "SRT1409 - 000",
                          "W752222 - 000",
                          "W753219 - 000",
                          "G537 - 000",
                          "G488",
                          "ISO001 - 000",
                          "W752375 - 000",
                          "W752374",
                          "G1",
                          "G2",
                          "P1"], subcomp_names)

    def test_find_col_idx(self):
        b_cad = get_cad_application()
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36_test.dwg"
        doc = b_cad.Documents.Open(template_path)
        table = doc.HandleToObject("7334F")
        col_idx = find_col_idx(table, "PART NUMBER")
        self.assertEqual(2, col_idx)
        doc.Close()

    def test_find_row_idx(self):
        b_cad = get_cad_application()
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36_test.dwg"
        doc = b_cad.Documents.Open(template_path)
        table = doc.HandleToObject("7334F")
        row_idx = find_row_idx(table, 2, "G488")
        self.assertEqual(10, row_idx)
        doc.Close()

    def test_find_part_table(self):
        b_cad = get_cad_application()
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36_test.dwg"
        doc = b_cad.Documents.Open(template_path)
        table = find_part_table(doc)
        self.assertEqual(doc.HandleToObject("7334F"), table)
        doc.Close()

    def test_assembly(self):
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36_test.dwg"
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "testdata")
        assembly = Assembly("TestAssembly01")
        assembly.copy_to_directory(template_path, directory)
        self.assertTrue(os.path.exists(os.path.join(directory, "TestAssembly01.dwg")))
        assembly.open()
        assembly.update_parameters({"MW": 100})

        # find the parametric dimension object
        for obj in assembly.doc.ModelSpace:
            if obj.Layer == "*ADSK_CONSTRAINTS":
                expression = obj.TextOverride.split("=")
                if expression[0] == "MW":
                    self.assertEqual("100", expression[1])
                    assembly.delete_constraints()
                    break
        const_len = len([obj for obj in assembly.doc.ModelSpace if obj.Layer == "*ADSK_CONSTRAINTS"])
        self.assertEqual(0, const_len)
        assembly.save_and_close()
        os.remove(assembly.path)
        os.remove(os.path.splitext(assembly.path)[0] + ".bak")

    def test_part(self):
        template_path = "H:/Desktop/projects/parametric blocks programming/DEMO/W753213-003_test.dwg"
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "testdata")
        part = Part("TestPart01")
        part.copy_to_directory(template_path, directory)
        self.assertTrue(os.path.exists(os.path.join(directory, "TestPart01.dwg")))
        part.open()
        part.update_parameters({"LENGTH": 30})

        # find the annotation dimension object
        dim = part.doc.HandleToObject("84B32")
        expression = dim.TextOverride
        self.assertEqual("30", expression)
        part.save_and_close()
        os.remove(part.path)
        os.remove(os.path.splitext(part.path)[0] + ".bak")
