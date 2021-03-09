from sympy import *
import sympy.physics.units as u
from IPython.display import display, Markdown
import pint


UNIT = pint.UnitRegistry()
UNIT.default_system = 'SI'   # setting default unit system
                             # choices are ['Planck', 'SI', 'US',
                             # 'atomic', 'cgs', 'imperial', 'mks']
# LATEX_CONTENT = ["\\begin{align}", "\\end{align}"]


class EquationWriter:
    def __init__(self, h_space, font_style, font_size):
        self.h_space = h_space
        self.font_style = font_style
        self.font_size = font_size
        self.equation_namespace = {}

    def define(self, equation, pref_unit="dimensionless", evaluate=False, num_decimal=2, inline=False):
        # annotation, pref_units, decimals, printout, inline
        left_expr, right_expr = equation.split("=")
        left_expr = left_expr.strip()
        right_expr = right_expr.strip()

        if pref_unit != "dimensionless":
            unit_obj = self.__unitstr2unitsympy(pref_unit)
            if unit_obj is None:
                return
        else:
            unit_obj = 1

        # convert a string equation to a sympy equation
        parse_lhs = parse_expr(left_expr)
        parse_rhs = parse_expr(right_expr) * unit_obj
        sym_eq = Eq(parse_lhs, parse_rhs)

        # convert sympy equation to latex equation.
        eq_latex = self.__convert_to_latex(sym_eq)

        if evaluate:
            res_eq = self.__evaluate(sym_eq, num_decimal)
            # update the equation namespace
            self.__add_eq_to_namespace(res_eq)
            res_eq_latex = self.__convert_to_latex(res_eq)
            if inline:
                res_eq = res_eq_latex.split("$")[1]
                eq = eq_latex.split("$")[1]
                res_eq_rhs = res_eq.split("=")[1].strip()
                out_latex = "${} = {}$".format(eq, res_eq_rhs)
            else:
                out_latex = "{}<br>{}".format(eq_latex, res_eq_latex)
        else:
            # add the equation to the namespace
            self.__add_eq_to_namespace(sym_eq)
            out_latex = eq_latex
        display(Markdown(out_latex))

    def __evaluate(self, equation, num_decimal):
        # get only the needed variables for substitution
        var_list = list(equation.rhs.atoms(Symbol))
        var_sub_dict = {}
        for sym_var in var_list:
            sym_var_str = str(sym_var)
            var_sub_dict.update({sym_var_str: self.equation_namespace[sym_var_str]})
        res_equation = equation.subs(var_sub_dict).evalf()
        res_equation = self.__round_expr(res_equation, num_decimal)
        if len(res_equation.rhs.atoms(Number)) == 1:  # this means its a y = x * unit
            # simplify it more using pint
            # convert sym eq to pint eq
            pint_eq = UNIT(str(res_equation.rhs)).to_compact().to_reduced_units()
            # convert back to sym_eq
            sym_unit = self.__unitstr2unitsympy(str(pint_eq.units))
            res_equation = Eq(res_equation.lhs, parse_expr(str(pint_eq.magnitude)) * sym_unit)
        return res_equation

    def __unitstr2unitsympy(self, str_unit):
        unit_obj = None
        try:
            # converting string unit input to a Sympy unit object
            unit_obj = eval("u.{}".format(str_unit))
        except (AttributeError, SyntaxError):
            print("You have entered an invalid unit. Units are case-sensitive.")
        return unit_obj

    def __round_expr(self, expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})

    def __convert_to_latex(self, s):
        '''
        Desc
        ====
            Converts sympy equation to latex equation
        parameters
        ==========
            s:sympy equation - equation in sympy.
        returns
        =======
            res_latex:latex - equation in latex
        '''
        res_latex = "${}$".format(latex(s, mul_symbol='dot'))
        return res_latex

    def __add_eq_to_namespace(self, equation):
        '''
        Desc
        ====
            Adds sympy equation to namespace list
        parameters
        ==========
            equation:sympy equation - equation in sympy
        returns
        =======
            None
        '''
        self.equation_namespace.update({str(equation.lhs): equation.rhs})


class HeaderWriter:
    def write(self):
        pass


class TitleWriter:
    def write(self):
        pass


class ImageWriter:
    def write(self):
        pass


class TableWriter:
    def write(self):
        pass


class GraphWriter:
    def setup(self):
        pass

    def write(self):
        pass

