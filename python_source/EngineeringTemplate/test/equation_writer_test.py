import unittest
from src.ptcc_module import EquationWriter
from sympy import *


class EquationWriterTest(unittest.TestCase):
    def test_define_001(self):
        eq_writer = EquationWriter(0, None, None)
        eq_writer.define("var_v = 1")
        self.assertEqual(eq_writer.equation_namespace["var_v"], parse_expr("1"))

    def test_define_002(self):
        eq_writer = EquationWriter(0, None, None)
        eq_writer.define("var_a = var_w * (var_v + var_x - var_y) / (varz * 3)")
        self.assertEqual(eq_writer.equation_namespace["var_a"], parse_expr("var_w * (var_v + var_x - var_y) / (varz * 3)"))

    def test_define_003(self):
        eq_writer = EquationWriter(0, None, None)
        eq_writer.define("var_v = 15")
        eq_writer.define("var_w = 2")
        eq_writer.define("var_x = 30")
        eq_writer.define("var_y = 4")
        eq_writer.define("var_z = 5")
        eq_writer.define("var_a = var_w * (var_v + var_x - var_y) / (var_z * 3)", evaluate=True)

    def test_define_004(self):
        eq_writer = EquationWriter(0, None, None)
        eq_writer.define("var_a = integrate(var_b ** 2)")

    def test_define_005(self):
        eq_writer = EquationWriter(0, None, None)
