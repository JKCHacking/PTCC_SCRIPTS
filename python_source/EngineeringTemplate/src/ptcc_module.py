from sympy import *
import sympy.physics.units as u
from IPython.display import display, Markdown
import pint
from pint.errors import UndefinedUnitError


UNIT = pint.UnitRegistry()
UNIT.default_system = 'SI'   # setting default unit system
                             # choices are ['Planck', 'SI', 'US',
                             # 'atomic', 'cgs', 'imperial', 'mks']


class EquationWriter:
    def __init__(self, h_space, font_name, font_size):
        self.h_space = str(h_space) + "in"
        self.font_name = font_name
        self.font_size = str(font_size) + "pt"
        self.equation_namespace = {}
        self.output = "<table>"

    def define(self, equation, annots=None, pref_unit="dimensionless", evaluate=False, num_decimal=2, inline=False):
        """
            Desc
            ====
            Interface method for defining and simplifying equations.

            Parameters
            ==========
            :param equation:str - Equation in string form. example: "y = m * x + b"
            :param annots:list - List of strings to use for annotating the equation. the first item in the list will be the
                                 primary annotation and the other items will be the secondary annotations.
            :param pref_unit:str - Unit to use for the equation. Please check Sympy Documentation for all the supported
                                   units.
            :param evaluate:bool - If True, the variables in the equation will be substitute by values defined and
                                   simplify the equation.
            :param num_decimal:int - number of decimal places to be displayed in the result. This will only work if evaluate
                                     is True.
            :param inline:bool - If True, the resulting equation will be in the same line with the original equation.
                                 If False, the resulting equation will be in the new line from the original equation.
                                 This will only work if evaluate is True.

            Returns
            =======
            :return: None
        """
        if equation.count("=") != 1:
            print("You entered an invalid Equation.")
            return

        primary_annotation = ""
        secondary_annotations = ""
        if annots:
            primary_annotation = annots[0]
            secondary_annotations = "<br>".join(annots[1:])

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
        try:
            parse_lhs = parse_expr(left_expr)
            parse_rhs = parse_expr(right_expr) * unit_obj
        except SyntaxError:
            print("You have entered an invalid equation.")
            return

        sym_eq = Eq(parse_lhs, parse_rhs)
        # convert sympy equation to latex string.
        eq_latex = self.__convert_to_latex(sym_eq)

        if evaluate:
            res_eq = self.__evaluate(sym_eq)
            res_eq = self.__round_expr(res_eq, num_decimal)
            # update the equation namespace
            self.__add_eq_to_namespace(res_eq)
            res_eq_latex = self.__convert_to_latex(res_eq)
            if inline:
                res_eq_rhs = res_eq.split("=")[1].strip()
                out_latex = "{} = {}".format(eq_latex, res_eq_rhs)
                output_local = self.__create_markdown(out_latex,
                                                      self.h_space,
                                                      primary_annotation,
                                                      secondary_annotations)
            else:
                output_local = self.__create_markdown(eq_latex,
                                                      self.h_space,
                                                      primary_annotation,
                                                      secondary_annotations)
                output_local += self.__create_markdown(res_eq_latex, self.h_space)
        else:
            sym_eq = self.__round_expr(sym_eq, num_decimal)
            # add the equation to the namespace
            self.__add_eq_to_namespace(sym_eq)
            output_local = self.__create_markdown(eq_latex,
                                                  self.h_space,
                                                  primary_annotation,
                                                  secondary_annotations)
        self.output += output_local

    def show(self):
        """
            Desc
            ====
            An Interface Method that displays the markdown result of all equations accumulated in the equation
            namespace. every succeeding call of this method will clear all the equations in the equation namespace.

            Parameters
            ==========
            None

            Returns
            =======
            :return: None
        """
        self.output += "</table>"
        display(Markdown(self.output))
        self.output = "<table>"

    def __evaluate(self, equation):
        """
            Desc
            ====
            This method will evaluate the equation, that is will substitute all the variables in the equation
            with their corresponding values previously defined in the equation namespace. It will also simplify the
            final result by using the base unit of its dimension.

            Parameters
            ==========
            :param equation:Sympy.Equality - Sympy Equation.

            Returns
            =======
            :return: res_equation:Sympy.Equality - The resulting equation after evaluation.
        """
        # get only the needed variables for substitution
        var_list = list(equation.rhs.atoms(Symbol))
        var_sub_dict = {}
        for sym_var in var_list:
            try:
                sym_var_str = str(sym_var)
                var_sub_dict.update({sym_var_str: self.equation_namespace[sym_var_str]})
            except KeyError:
                pass
        res_equation = equation.subs(var_sub_dict).evalf()
        # added redundancy for integral, derivatives, etc.
        res_equation = res_equation.doit()
        if len(res_equation.rhs.atoms(u.Quantity)) != 0:
            try:
                # simplify it more using pint, convert sym eq to pint eq
                pint_eq = UNIT(str(res_equation.rhs)).to_compact().to_reduced_units()

                # convert back to sym_eq
                if str(pint_eq.units) != "dimensionless":
                    sym_unit = self.__unitstr2unitsympy(str(pint_eq.units))
                    res_equation = Eq(res_equation.lhs, parse_expr(str(pint_eq.magnitude)) * sym_unit)
                else:
                    res_equation = Eq(res_equation.lhs, parse_expr(str(pint_eq.magnitude)))
            except UndefinedUnitError:
                pass
        return res_equation

    def __unitstr2unitsympy(self, str_unit):
        """
            Desc
            ====
            Method to convert unit in string to sympy unit.

            Parameters
            ==========
            :param str_unit: str - Unit name in string.

            Returns
            =======
            :return: unit_obj:sympyunit - Sympy unit
        """
        unit_obj = None
        try:
            # converting string unit input to a Sympy unit object
            unit_obj = eval("u.{}".format(str_unit))
        except (AttributeError, SyntaxError):
            print("You have entered an invalid unit: {}. Note: Units are case-sensitive.".format(str_unit))
        return unit_obj

    def __round_expr(self, equation, num_digits):
        """
            Desc
            ====
            Method for rounding all the number in the equation.

            Parameters
            ==========
            :param equation:sympy equation - Sympy Equation to be rounded off.
            :param num_digits:int - number of decimal places to be rounded off in each number in the equation.

            Returns
            =======
            :return:sympy equation - Equation with rounded Numbers.
        """
        return equation.xreplace({n: round(n, num_digits) for n in equation.atoms(Number)})

    def __convert_to_latex(self, s):
        """
            Desc
            ====
                Converts sympy equation to latex equation
            parameters
            ==========
                s:sympy equation - equation in sympy.
            returns
            =======
                res_latex:string - equation in latex
        """
        res_latex = "{}".format(latex(s, mul_symbol='dot'))
        return res_latex

    def __add_eq_to_namespace(self, equation):
        """
            Desc
            ====
                Adds sympy equation to namespace list
            parameters
            ==========
                equation:sympy equation - equation in sympy
            returns
            =======
                None
        """
        self.equation_namespace.update({str(equation.lhs): equation.rhs})

    def __create_markdown(self, eq_str, hspace="0", primary_annot="", secondary_annot=""):
        """
            Desc
            ====
            Method that creates a markdown for displaying result in jupyter notebook.

            Parameters
            ==========
            :param eq_str:str - Equation string in latex format.
            :param hspace:str - Measured in Inches, length of the horizontal space between the equation and the annotations.
            :param primary_annot: The primary annotation (annotation inline with the equation).
            :param secondary_annot: The secondary annotations (annotations under the primary annotation).

            Returns
            =======
            :return: None
        """
        eq_markdown = "<tr style='background-color:#ffffff;'>"\
                            "<td style='vertical-align:top; text-align:left; font-family:{font_name}, Arial; font-size: {font_size};'>" \
                                "${eq_str}$" \
                            "</td>"\
                            "<td>" \
                                "$\\hspace{{{hspace}}}$" \
                            "</td>"\
                            "<td style='text-align:left;font-family:{font_name}, Arial;'>" \
                                "<div style='font-size:{font_size};'>{p_annot}</div>" \
                                "<div style='font-size:{font_size}; font-style:italic;'>{s_annots}</div>" \
                            "</td>"\
                      "</tr>".format(eq_str=eq_str, hspace=hspace, p_annot=primary_annot, s_annots=secondary_annot,
                                     font_name=self.font_name, font_size=self.font_size)
        return eq_markdown


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

