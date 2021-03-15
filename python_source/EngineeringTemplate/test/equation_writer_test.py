import unittest
from src.ptcc_module import EquationWriter
from sympy import *
import sympy.physics.units as u


class EquationWriterTest(unittest.TestCase):
    def typical_settings(self):
        hspace = 2
        font_name = "Times New Roman"
        font_size = 12
        eq_writer = EquationWriter(hspace, font_name, font_size)
        return eq_writer

    def test_define_001(self):
        '''
        Test equation with fraction
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("y = x/2")
        self.assertEqual("0.5*x", str(eq_writer.equation_namespace["y"]))

    def test_define_002(self):
        '''
        Test equation with fraction and units.
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("y = x/z", pref_unit="m")
        self.assertEqual("meter*x/z", str(eq_writer.equation_namespace["y"]))

    def test_define_003(self):
        '''
        Test equation with integrals
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("y = Integral(x**2)")
        self.assertEqual("Integral(x**2, x)", str(eq_writer.equation_namespace["y"]))

    def test_define_004(self):
        '''
        Test simplifying integral equation
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("x = 2", pref_unit="m")
        eq_writer.define("y = Integral(x**2)", evaluate=True)
        self.assertEqual("2.67*meter**3", str(eq_writer.equation_namespace['y']))

    def test_define_005(self):
        '''
        Test Derivative equations
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("y = Derivative(x**2)")
        self.assertEqual("Derivative(x**2, x)", str(eq_writer.equation_namespace['y']))

    def test_define_006(self):
        '''
        Test simplifying Derivatives
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("x = 2", pref_unit="m")
        eq_writer.define("y = Derivative(x**2)", evaluate=True)
        self.assertEqual("4*meter", str(eq_writer.equation_namespace['y']))

    def test_define_007(self):
        '''
        Test equation with summation
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("y = Sum(x**i, (i, 0, 5))")
        self.assertEqual("Sum(x**i, (i, 0, 5))", str(eq_writer.equation_namespace['y']))

    def test_define_008(self):
        '''
        Test simplifying summation equation
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("x = 5")
        eq_writer.define("y = Sum(x*i, (i, 0, 5))", evaluate=True)
        self.assertEqual("75", str(eq_writer.equation_namespace['y']))

    def test_define_009(self):
        '''
        Test annotations
        '''
        annots = ["Primary Annotation Test", "Secondary Annotation Test1", "Secondary Annotation Test2"]
        eq_writer = self.typical_settings()
        eq_writer.define("y = x**2", annots=annots)
        self.assertTrue("Annotation Test" in eq_writer.output)
        self.assertTrue("Secondary Annotation Test1" in eq_writer.output)
        self.assertTrue("Secondary Annotation Test2" in eq_writer.output)
        self.assertTrue("<br>" in eq_writer.output)

    def test_define_010(self):
        '''
        Test annotations
        '''
        annots = ["Primary Annotation Test", "Secondary Annotation Test1"]
        eq_writer = self.typical_settings()
        eq_writer.define("y = x**2", annots=annots)
        self.assertTrue("Annotation Test" in eq_writer.output)
        self.assertTrue("Secondary Annotation Test1" in eq_writer.output)
        self.assertTrue("<br>" not in eq_writer.output)

    def test_define_011(self):
        '''
        Test decimal place
        '''
        num_decimal = 10
        eq_writer = self.typical_settings()
        eq_writer.define("x = 3 * pi", evaluate=True, num_decimal=num_decimal)
        self.assertEqual(num_decimal, len(str(eq_writer.equation_namespace["x"]).split(".")[1]))

    def test_define_012(self):
        '''
        Test decimal Place
        '''
        num_decimal = 2
        eq_writer = self.typical_settings()
        eq_writer.define("x = 2 * 1.223491823091283012983", evaluate=True)
        self.assertEqual(num_decimal, len(str(eq_writer.equation_namespace["x"]).split(".")[1]))

    def test_define_013(self):
        '''
        Test Non Equation string
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("Hello World")
        self.assertEqual(0, len(eq_writer.equation_namespace))

    def test_define_014(self):
        '''
        Test Double Equation string
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("x = y = z")
        self.assertEqual(0, len(eq_writer.equation_namespace))

    def test_define_015(self):
        '''
        Test Non Equation string
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("He=llo World")
        self.assertEqual(0, len(eq_writer.equation_namespace))

    def test_define_016(self):
        '''
        Test simplifying equations with units.
        result is a b = a * unit
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("x = 1", pref_unit="m")
        eq_writer.define("w = 1", pref_unit="m")
        eq_writer.define("y = x + w", evaluate=True)
        self.assertEqual("2.0*meter", str(eq_writer.equation_namespace["y"]))

    def test_define_017(self):
        '''
        Test simplifying equations with units.
        result is a b = a (dimensionless/unitless)
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", pref_unit="m")
        eq_writer.define("w = 5", pref_unit="m")
        eq_writer.define("y = x / w", evaluate=True)
        self.assertEqual(0, len(eq_writer.equation_namespace['y'].atoms(u.Quantity)))
        self.assertEqual(parse_expr("2"), eq_writer.equation_namespace['y'])

    def test_define_018(self):
        '''
        Test simplifying equations with units.
        result is a b = a * unitsub1/unitsub2 (units with the same base unit)
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", pref_unit="cm")
        eq_writer.define("w = 5", pref_unit="mm")
        eq_writer.define("y = x / w", evaluate=True)
        self.assertEqual(0, len(eq_writer.equation_namespace['y'].atoms(u.Quantity)))
        self.assertEqual(parse_expr("20"), eq_writer.equation_namespace['y'])

    def test_define_019(self):
        '''
        Test simplifying equations with units.
        result is a b = a * unitsub1 + c * unitsub2 (units with the same base unit)
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", pref_unit="cm")
        eq_writer.define("w = 5", pref_unit="mm")
        eq_writer.define("y = x + w", evaluate=True)
        self.assertEqual(1, len(eq_writer.equation_namespace['y'].atoms(u.Quantity)))
        self.assertEqual("105.0*millimeter", str(eq_writer.equation_namespace['y']))

    def test_define_020(self):
        '''
        Test simplifying equations with units.
        result is a b = a * unit + c (with unknown variable)
        '''

        eq_writer = self.typical_settings()
        eq_writer.define("x = 10", pref_unit="cm")
        eq_writer.define("w = 5", pref_unit="mm")
        eq_writer.define("y = x + w + z", evaluate=True)
        self.assertEqual(2, len(eq_writer.equation_namespace['y'].atoms(u.Quantity)))
        self.assertEqual("10.0*centimeter + 5.0*millimeter + z", str(eq_writer.equation_namespace['y']))

    def test_define_021(self):
        '''
        Test very long equation
        '''
        eq_writer = self.typical_settings()
        eq_writer.define("var_v = 15")
        eq_writer.define("var_w = 2")
        eq_writer.define("var_x = 30")
        eq_writer.define("var_y = 4")
        eq_writer.define("var_z = 5")
        eq_writer.define("var_a = var_w * (var_v + var_x - var_y) / (var_z * 3)", evaluate=True)
        self.assertEqual("5.47", str(eq_writer.equation_namespace["var_a"]))
