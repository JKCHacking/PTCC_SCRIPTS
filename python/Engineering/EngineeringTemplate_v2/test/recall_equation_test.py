import unittest
import sympy.physics.units as u
from src.ptcc_module import Controller
from sympy import *


class RecallEquationTest(unittest.TestCase):
    def typical_settings(self):
        hspace = "2in"
        font_name = "Times New Roman"
        font_size = "12pt"
        image_folder_name = "Test"
        controller = Controller(font_name, font_size, hspace, image_folder_name)
        return controller

    def test_recall_equation_001(self):
        controller = self.typical_settings()
        controller.create_equation("y = m_1 * x + b")
        actual = controller.recall_equation("y")
        expected = sympify("m_1 * x + b")
        self.assertEqual(expected, actual)

    def test_recall_equation_002(self):
        controller = self.typical_settings()
        controller.create_equation("x = 1 * m")
        controller.create_equation("w = 1 * m")
        controller.create_equation("y = x + w", simplify=True)
        actual = controller.recall_equation("y")
        expected = round(2.0, 2) * u.meter
        self.assertEqual(expected, actual)
