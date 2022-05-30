import unittest
from src.ptcc_module import Controller, EQUATION_NAMESPACE
from sympy import *
import sympy.physics.units as u


class CreateEquationTest(unittest.TestCase):
    def typical_settings(self):
        hspace = "2in"
        font_name = "Times New Roman"
        font_size = "12pt"
        image_folder_name = "Test"
        controller = Controller(font_name, font_size, hspace, image_folder_name)
        return controller

    def test_create_equation_001(self):
        """
        Test equation with fraction
        """
        controller = self.typical_settings()
        actual = controller.create_equation("y = x/2")
        expected = sympify("x/2")
        self.assertTrue(Eq(expected, actual))

    def test_create_equation_002(self):
        """
        Test equation with integrals
        """
        controller = self.typical_settings()
        actual = controller.create_equation("y = Integral(x**2)")
        expected = Integral(parse_expr("x ** 2"), parse_expr("x"))
        self.assertEqual(expected, actual)

    def test_create_equation_003(self):
        """
        Test simplifying integral equation
        """
        controller = self.typical_settings()
        controller.create_equation("x = 2 * m")
        actual = controller.create_equation("y = Integral(x**2)", simplify=True)
        expected = Float(2.67, 3) * (u.m ** 3)
        self.assertEqual(expected, actual)

    def test_create_equation_004(self):
        """
        Test Derivative equations
        """
        controller = self.typical_settings()
        actual = controller.create_equation("y = Derivative(x**2)")
        expected = Derivative(parse_expr("x ** 2"))
        self.assertEqual(expected, actual)

    def test_create_equation_005(self):
        """
        Test simplifying Derivatives
        """
        controller = self.typical_settings()
        controller.create_equation("x = 2 * m")
        actual = controller.create_equation("y = Derivative(x**2)", simplify=True)
        expected = 4.0 * u.meter
        self.assertEqual(expected, actual)

    def test_create_equation_006(self):
        """
        Test equation with summation
        """
        controller = self.typical_settings()
        actual = controller.create_equation("y = Sum(x**i, (i, 0, 5))")
        expected = parse_expr("Sum(x ** i, (i, 0, 5))")
        self.assertEqual(expected, actual)

    def test_create_equation_007(self):
        """
        Test simplifying summation equation
        """
        controller = self.typical_settings()
        controller.create_equation("x = 5")
        actual = controller.create_equation("y = Sum(x*i, (i, 0, 5))", simplify=True)
        expected = round(75, 2)
        self.assertEqual(expected, actual)

    def test_create_equation_008(self):
        """
        Test decimal place
        """
        num_decimal = 10
        controller = self.typical_settings()
        controller.create_equation("z = 3")
        actual = controller.create_equation("x = z * pi", simplify=True, num_decimal=num_decimal)
        self.assertEqual(num_decimal, len(str(actual).split(".")[1]))

    def test_create_equation_009(self):
        """
        Test decimal Place
        """
        num_decimal = 2
        controller = self.typical_settings()
        actual = controller.create_equation("x = 2 * 1.223491823091283012983", simplify=True)
        self.assertEqual(num_decimal, len(str(actual).split(".")[1]))

    def test_create_equation_010(self):
        """
        Test Non Equation string
        """

        controller = self.typical_settings()
        actual = controller.create_equation("Hello World")
        self.assertEqual(None, actual)

    def test_create_equation_011(self):
        """
        Test Double Equation string
        """

        controller = self.typical_settings()
        actual = controller.create_equation("x = y = z")
        self.assertEqual(None, actual)

    def test_create_equation_012(self):
        """
        Test Non Equation string
        """

        controller = self.typical_settings()
        actual = controller.create_equation("He=llo World")
        self.assertEqual(None, actual)

    def test_create_equation_013(self):
        """
        Test simplifying equations with units.
        result is a b = a * unit
        """
        controller = self.typical_settings()
        controller.create_equation("x = 1 * m")
        controller.create_equation("w = 1 * m")
        actual = controller.create_equation("y = x + w", simplify=True)
        self.assertEqual(round(2.0, 2) * u.meter, actual)

    def test_create_equation_014(self):
        """
        Test simplifying equations with units.
        result is a b = a (dimensionless/unitless)
        """

        controller = self.typical_settings()
        controller.create_equation("x = 10 * m")
        controller.create_equation("w = 5 * m")
        actual = controller.create_equation("y = x / w", simplify=True)
        self.assertEqual(0, len(actual.atoms(u.Quantity)))
        self.assertEqual(parse_expr("2"), actual)

    def test_create_equation_015(self):
        """
        Test simplifying equations with units.
        result is a b = a * unitsub1/unitsub2 (units with the same base unit)
        """

        controller = self.typical_settings()
        controller.create_equation("x = 10 * cm")
        controller.create_equation("w = 5 * mm")
        actual = controller.create_equation("y = x / w", simplify=True)
        self.assertEqual(0, len(actual.atoms(u.Quantity)))
        self.assertEqual(20, int(actual))

    def test_create_equation_016(self):
        """
        Test simplifying equations with units.
        result is a b = a * unitsub1 + c * unitsub2 (units with the same base unit)
        """

        controller = self.typical_settings()
        controller.create_equation("x = 10 * cm")
        controller.create_equation("w = 5 * mm")
        actual = controller.create_equation("y = x + w", simplify=True)
        self.assertEqual(1, len(actual.atoms(u.Quantity)))
        self.assertEqual(10.5 * u.cm, actual)

    def test_create_equation_017(self):
        """
        Test simplifying equations with units.
        result is a b = a * unit + c (with unknown variable)
        """

        controller = self.typical_settings()
        controller.create_equation("x = 10 * cm")
        controller.create_equation("w = 5 * mm")
        actual = controller.create_equation("y = x + w + a_1", simplify=True)
        self.assertEqual(1, len(actual.atoms(u.Quantity)))
        self.assertEqual(10.5 * u.centimeter + symbols("a_1"), actual)

    def test_create_equation_018(self):
        """
        Test very long equation
        """
        controller = self.typical_settings()
        controller.create_equation("var_v = 15")
        controller.create_equation("var_w = 2")
        controller.create_equation("var_x = 30")
        controller.create_equation("var_y = 4")
        controller.create_equation("var_z = 5")
        actual = controller.create_equation("var_a = var_w * (var_v + var_x - var_y) / (var_z * 3)", simplify=True)
        self.assertEqual(Float(5.47, 3), actual)

    def test_create_equation_019(self):
        """
        Test for simplifying equation to expression.
        """
        controller = self.typical_settings()
        controller.create_equation("x = 10 * cm")
        actual = controller.create_equation("W_max = x + 2", simplify=True)
        self.assertEqual(10.0 * u.centimeter + 2.0, actual)

    def test_create_equation_020(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 1000 * MPa", simplify=True)
        self.assertEqual(1000.0 * u.MPa, actual)

    def test_create_equation_021(self):
        controller = self.typical_settings()
        controller.create_equation("x = 4 * N")
        controller.create_equation("w = 2 * mm ** 2")
        actual = controller.create_equation("y = x / w", convert_to="MPa", simplify=True)
        self.assertEqual(2.0 * u.megapascal, actual)

    def test_create_equation_022(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 2 * N/mm ** 2")
        self.assertEqual(2 * u.newton/u.millimeter**2, actual)

    def test_create_equation_023(self):
        controller = self.typical_settings()
        controller.create_equation("x = 4 * newton")
        controller.create_equation("y = 3 * mm")
        actual = controller.create_equation("w = x / y ** 2", convert_to="MPa", simplify=True)
        expected = Float(0.44, 2) * u.megapascal
        self.assertEqual(expected, actual)

    def test_create_equation_024(self):
        controller = self.typical_settings()
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
            controller.create_equation("x{} = 1 * {}".format(i, unit))
        for i, unit in enumerate(unit_list):
            self.assertEqual(unit, str(EQUATION_NAMESPACE["x{}".format(i)].equation.rhs))

    def test_create_equation_025(self):
        controller = self.typical_settings()
        q = controller.create_equation("q = 5 * m")
        controller.add_eq_to_namespace(DoubleQ=2 * q)
        actual = controller.create_equation("z = DoubleQ * 2", simplify=True)
        expected = 20.0 * u.m
        self.assertEqual(expected, actual)

    def test_create_equation_026(self):
        controller = self.typical_settings()
        q = controller.create_equation("q = 5 * m")
        controller.add_eq_to_namespace(DoubleQ=2 * q)
        actual = controller.create_equation("z = DoubleQ * 2", simplify=True)
        expected = 20.0 * u.m
        self.assertEqual(expected, actual)

    def test_create_equation_027(self):
        controller = self.typical_settings()
        q = controller.create_equation("q = 5 * m")
        DoubleQ = 2 * q
        controller.add_eq_to_namespace(DoubleQ=DoubleQ)
        actual = controller.create_equation("z = DoubleQ * 2", simplify=True)
        expected = 20.0 * u.m
        self.assertEqual(expected, actual)

    def test_create_equation_028(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 5 * N")
        expected = 5 * u.newton
        self.assertEqual(actual, expected)

    def test_create_equation_029(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 4*N+2")
        expected = 4 * u.newton + 2
        self.assertEqual(actual, expected)

    def test_create_equation_030(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = (2 * N + 1) * g")
        expected = (2 * u.newton + 1) * u.gram
        self.assertEqual(actual, expected)

    def test_create_equation_031(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = (3 + 2 * N)")
        expected = (3 + 2 * u.newton)
        self.assertEqual(actual, expected)

    def test_create_equation_032(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = (3 + 2 * saN)")
        expected = (3 + 2 * symbols("saN"))
        self.assertEqual(actual, expected)

    def test_create_equation_033(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 5 * Newyear")
        expected = (5 * symbols("Newyear"))
        self.assertEqual(actual, expected)

    def test_create_equation_034(self):
        controller = self.typical_settings()
        actual = controller.create_equation("x = 5 * Q")
        expected = (5 * symbols("Q"))
        self.assertEqual(actual, expected)

    # =========================================ARRAY TESTS====================================================
    def test_create_equation_035(self):
        controller = self.typical_settings()
        controller.create_equation("z = Array([1, 2, 3, 4])")
        self.assertRaises(TypeError, controller.create_equation, "x = z + 10 * cm", simplify=True)

    def test_create_equation_036(self):
        controller = self.typical_settings()
        controller.create_equation("x = Array([1, 2, 3, 4])")
        controller.create_equation("w = Array([4, 5, 6, 7])")
        actual = controller.create_equation("z = x + w", simplify=True)
        expected = Array([5, 7, 9, 11])
        self.assertEqual(expected, actual)

    def test_create_equation_037(self):
        controller = self.typical_settings()
        controller.create_equation("z = Array([1, 2, 3, 4])")
        actual = controller.create_equation("x = z * 10 * cm", simplify=True)
        expected = Array([10 * u.cm, 20 * u.cm, 30 * u.cm, 40 * u.cm])
        self.assertEqual(expected, actual)

    def test_create_equation_038(self):
        controller = self.typical_settings()
        actual = controller.create_equation("y = 4 * Array([1, 2, 3, 4])", simplify=True)
        expected = Array([4, 8, 12, 16])
        self.assertEqual(expected, actual)

    def test_create_equation_039(self):
        controller = self.typical_settings()
        actual = controller.create_equation("y = 4 * Array([1, 2, 3, 4])")
        expected = Array([4, 8, 12, 16])
        self.assertEqual(expected, actual)

    def test_create_equation_040(self):
        controller = self.typical_settings()
        actual = controller.create_equation("y = 4 * Array([1 * N, 2, 3, 4])")
        expected = Array([4 * u.newton, 8, 12, 16])
        self.assertEqual(expected, actual)

    def test_create_equation_041(self):
        controller = self.typical_settings()
        actual = controller.create_equation("y = Array([1 * N, 2 * m, 3, 4])")
        expected = Array([1 * u.newton, 2 * u.meter, 3, 4])
        self.assertEqual(expected, actual)

