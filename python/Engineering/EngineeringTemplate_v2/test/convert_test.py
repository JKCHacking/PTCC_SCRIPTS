import unittest
from src.ptcc_module import Controller
import sympy.physics.units as u


class ConvertTest(unittest.TestCase):
    def typical_settings(self):
        hspace = "2in"
        font_name = "Times New Roman"
        font_size = "12pt"
        image_folder_name = "Test"
        controller = Controller(font_name, font_size, hspace, image_folder_name)
        return controller

    def test_convert_001(self):
        controller = self.typical_settings()
        controller.create_equation("y = 3000 * m")
        actual = controller.convert("y", "km")
        expected = 3.0 * u.km
        self.assertEqual(expected, actual)
