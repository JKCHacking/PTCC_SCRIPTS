import unittest
from src.ptcc_module import EquationWriter, CustomDisplay
from sympy import *
import sympy.physics.units as u


class EquationWriterTest(unittest.TestCase):
    def typical_settings(self):
        hspace = 2
        font_name = "Times New Roman"
        font_size = 12
        self.c_display = CustomDisplay()
        eq_writer = EquationWriter(hspace, font_name, font_size, self.c_display)
        return eq_writer

    def test_define_001(self):
        """
        Test equation with fraction
        """
        eq_writer = self.typical_settings()
        actual = eq_writer.define("y = x/2")
        expected = sympify("x/2")
        self.assertTrue(Eq(expected, actual))

    def test_define_002(self):
        """
        Test equation with fraction and units.
        """
        eq_writer = self.typical_settings()
        actual = eq_writer.define("y = x/z", unit="m")
        expected = sympify("x/z") * u.m
        self.assertTrue(Eq(expected, actual))

    def test_define_003(self):
        """
        Test equation with integrals
        """
        eq_writer = self.typical_settings()
        actual = eq_writer.define("y = Integral(x**2)")
        expected = Integral(parse_expr("x ** 2"), parse_expr("x"))
        self.assertEqual(expected, actual)

    def test_define_004(self):
        """
        Test simplifying integral equation
        """
        eq_writer = self.typical_settings()
        eq_writer.define("x = 2", unit="m")
        actual = eq_writer.define("y = Integral(x**2)", simplify=True)
        expected = round(2.67, 2) * (u.m ** 3)
        self.assertTrue(expected, actual)

    def test_define_005(self):
        """
        Test Derivative equations
        """
        eq_writer = self.typical_settings()
        actual = eq_writer.define("y = Derivative(x**2)")
        expected = Derivative(parse_expr("x ** 2"))
        self.assertEqual(expected, actual)

    def test_define_006(self):
        """
        Test simplifying Derivatives
        """
        eq_writer = self.typical_settings()
        eq_writer.define("x = 2", unit="m")
        actual = eq_writer.define("y = Derivative(x**2)", simplify=True)
        expected = 4.0 * u.meter
        self.assertEqual(expected, actual)

    def test_define_007(self):
        """
        Test equation with summation
        """
        eq_writer = self.typical_settings()
        actual = eq_writer.define("y = Sum(x**i, (i, 0, 5))")
        expected = parse_expr("Sum(x ** i, (i, 0, 5))")
        self.assertEqual(expected, actual)

    def test_define_008(self):
        """
        Test simplifying summation equation
        """
        eq_writer = self.typical_settings()
        eq_writer.define("x = 5")
        actual = eq_writer.define("y = Sum(x*i, (i, 0, 5))", simplify=True)
        expected = round(75, 2)
        self.assertEqual(expected, actual)

    def test_define_009(self):
        """
        Test annotations
        """
        annots = ["Primary Annotation Test", "Secondary Annotation Test1", "Secondary Annotation Test2"]
        eq_writer = self.typical_settings()
        eq_writer.define("y = x**2", annots=annots)
        self.assertTrue("Annotation Test" in self.c_display.writer_output)
        self.assertTrue("Secondary Annotation Test1" in self.c_display.writer_output)
        self.assertTrue("Secondary Annotation Test2" in self.c_display.writer_output)
        self.assertTrue("<br>" in self.c_display.writer_output)

    def test_define_010(self):
        """
        Test annotations
        """
        annots = ["Primary Annotation Test", "Secondary Annotation Test1"]
        eq_writer = self.typical_settings()
        eq_writer.define("y = x**2", annots=annots)
        self.assertTrue("Annotation Test" in self.c_display.writer_output)
        self.assertTrue("Secondary Annotation Test1" in self.c_display.writer_output)
        self.assertTrue("<br>" not in self.c_display.writer_output)

    def test_define_011(self):
        """
        Test decimal place
        """
        num_decimal = 10
        eq_writer = self.typical_settings()
        eq_writer.define("z = 3")
        actual = eq_writer.define("x = z * pi", simplify=True, num_decimal=num_decimal)
        self.assertEqual(num_decimal, len(str(actual).split(".")[1]))

    def test_define_012(self):
        """
        Test decimal Place
        """
        num_decimal = 2
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 2 * 1.223491823091283012983", simplify=True)
        self.assertEqual(num_decimal, len(str(actual).split(".")[1]))

    def test_define_013(self):
        """
        Test Non Equation string
        """

        eq_writer = self.typical_settings()
        actual = eq_writer.define("Hello World")
        self.assertEqual(None, actual)

    def test_define_014(self):
        """
        Test Double Equation string
        """

        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = y = z")
        self.assertEqual(None, actual)

    def test_define_015(self):
        """
        Test Non Equation string
        """

        eq_writer = self.typical_settings()
        actual = eq_writer.define("He=llo World")
        self.assertEqual(None, actual)

    def test_define_016(self):
        """
        Test simplifying equations with units.
        result is a b = a * unit
        """
        eq_writer = self.typical_settings()
        eq_writer.define("x = 1", unit="m")
        eq_writer.define("w = 1", unit="m")
        actual = eq_writer.define("y = x + w", simplify=True)
        self.assertEqual(round(2.0, 2) * u.meter, actual)

    def test_define_017(self):
        """
        Test simplifying equations with units.
        result is a b = a (dimensionless/unitless)
        """

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", unit="m")
        eq_writer.define("w = 5", unit="m")
        actual = eq_writer.define("y = x / w", simplify=True)
        self.assertEqual(0, len(actual.atoms(u.Quantity)))
        self.assertEqual(parse_expr("2"), actual)

    def test_define_018(self):
        """
        Test simplifying equations with units.
        result is a b = a * unitsub1/unitsub2 (units with the same base unit)
        """

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", unit="cm")
        eq_writer.define("w = 5", unit="mm")
        actual = eq_writer.define("y = x / w", simplify=True)
        self.assertEqual(0, len(actual.atoms(u.Quantity)))
        self.assertEqual(20, int(actual))

    def test_define_019(self):
        """
        Test simplifying equations with units.
        result is a b = a * unitsub1 + c * unitsub2 (units with the same base unit)
        """

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", unit="cm")
        eq_writer.define("w = 5", unit="mm")
        actual = eq_writer.define("y = x + w", simplify=True)
        self.assertEqual(1, len(actual.atoms(u.Quantity)))
        self.assertEqual(10.5 * u.cm, actual)

    def test_define_020(self):
        """
        Test simplifying equations with units.
        result is a b = a * unit + c (with unknown variable)
        """

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", unit="cm")
        eq_writer.define("w = 5", unit="mm")
        actual = eq_writer.define("y = x + w + z", simplify=True)
        self.assertEqual(1, len(actual.atoms(u.Quantity)))
        self.assertEqual(10.5 * u.centimeter + symbols("z"), actual)

    def test_define_021(self):
        """
        Test very long equation
        """
        eq_writer = self.typical_settings()
        eq_writer.define("var_v = 15")
        eq_writer.define("var_w = 2")
        eq_writer.define("var_x = 30")
        eq_writer.define("var_y = 4")
        eq_writer.define("var_z = 5")
        actual = eq_writer.define("var_a = var_w * (var_v + var_x - var_y) / (var_z * 3)", simplify=True)
        self.assertEqual(Float(5.47, 3), actual)

    def test_define_022(self):
        """
        Test for simplifying equation to expression.
        """
        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", unit="cm")
        actual = eq_writer.define("W_max = x + 2", simplify=True)
        self.assertEqual(10.0 * u.centimeter + 2.0, actual)

    def test_define_023(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 1000 * MPa", simplify=True)
        self.assertEqual(1000.0 * u.MPa, actual)

    def test_define_024(self):
        eq_writer = self.typical_settings()
        eq_writer.define("x = 4", unit="N")
        eq_writer.define("w = 2", unit="mm ** 2")
        actual = eq_writer.define("y = x / w", unit="MPa", simplify=True)
        self.assertEqual(2.0 * u.megapascal, actual)

    def test_define_025(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 2", unit="N/mm ** 2")
        self.assertEqual(2 * u.newton/u.millimeter**2, actual)

    def test_define_026(self):
        eq_writer = self.typical_settings()
        eq_writer.define("x = 4 * newton")
        eq_writer.define("y = 3 * mm")
        eq_writer.define("z = x + y", simplify=True)
        actual = eq_writer.define("w = x / y ** 2", unit="MPa", simplify=True)
        expected = Float(0.44, 2) * u.megapascal
        self.assertEqual(expected, actual)

    def test_define_027(self):
        eq_writer = self.typical_settings()
        unit_list = ["pascal",
                     "megapascal",
                     "kilopascal",
                     "gigapascal",
                     "meter",
                     "kilometer",
                     "millimeter",
                     "newton",
                     "kilonewton",
                     "gram",
                     "kilogram",
                     "milligram",
                     "second",
                     "millisecond",
                     "microsecond",
                     "kelvin"]

        for i, unit in enumerate(unit_list):
            eq_writer.define("x{} = 1".format(i), unit=unit)
        for i, unit in enumerate(unit_list):
            self.assertEqual(unit, str(eq_writer.equation_namespace["x{}".format(i)]))

    def test_define_028(self):
        eq_writer = self.typical_settings()
        eq_writer.define("z = Array([1, 2, 3, 4])")
        self.assertRaises(TypeError, eq_writer.define, "x = z + 10 * cm", simplify=True)

    def test_define_029(self):
        eq_writer = self.typical_settings()
        eq_writer.define("x = Array([1, 2, 3, 4])")
        eq_writer.define("w = Array([4, 5, 6, 7])")
        actual = eq_writer.define("z = x + w", simplify=True)
        expected = Array([5, 7, 9, 11])
        self.assertEqual(expected, actual)

    def test_define_030(self):
        eq_writer = self.typical_settings()
        eq_writer.define("z = Array([1, 2, 3, 4])")
        actual = eq_writer.define("x = z * 10 * cm", simplify=True)
        expected = Array([10 * u.cm, 20 * u.cm, 30 * u.cm, 40 * u.cm])
        self.assertEqual(expected, actual)

    def test_define_031(self):
        eq_writer = self.typical_settings()
        q = eq_writer.define("q = 5 * m")
        eq_writer.add_equation(DoubleQ=2 * q)
        actual = eq_writer.define("z = DoubleQ * 2", simplify=True)
        expected = 20.0 * u.m
        self.assertEqual(expected, actual)

    def test_define_032(self):
        eq_writer = self.typical_settings()
        q = eq_writer.define("q = 5 * m")
        DoubleQ = 2 * q
        eq_writer.add_equation(DoubleQ=DoubleQ)
        actual = eq_writer.define("z = DoubleQ * 2", simplify=True)
        expected = 20.0 * u.m
        self.assertEqual(expected, actual)

    def test_define_033(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 5 * N")
        expected = 5 * u.newton
        self.assertEqual(actual, expected)

    def test_define_034(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 4*N+2")
        expected = 4 * u.newton + 2
        self.assertEqual(actual, expected)

    def test_define_035(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = (2 * N + 1) * g")
        expected = (2 * u.newton + 1) * u.gram
        self.assertEqual(actual, expected)

    def test_define_036(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = (3 + 2 * N)")
        expected = (3 + 2 * u.newton)
        self.assertEqual(actual, expected)

    def test_define_037(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = (3 + 2 * saN)")
        expected = (3 + 2 * symbols("saN"))
        self.assertEqual(actual, expected)

    def test_define_038(self):
        eq_writer = self.typical_settings()
        actual = eq_writer.define("x = 5 * Newyear")
        expected = (5 * symbols("Newyear"))
        self.assertEqual(actual, expected)
