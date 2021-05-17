import re as regular_expression
import sympy.physics.units as SYMPY_UNIT
import pint
from IPython.display import display, Markdown, HTML
from sympy import *
from pint.errors import UndefinedUnitError

EQUATION_NAMESPACE = {}
ANNOTATIONS = {}
EQUATION_HISTORY = {}

# initializing units
PINT_UNIT = pint.UnitRegistry()
# setting default unit system
PINT_UNIT.default_system = 'SI'  # choices are ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks']

# define all units that is not supported by Sympy but needed by PTCC
SYMPY_UNIT.megapascal = SYMPY_UNIT.Quantity("megapascal", abbrev="MPa")
SYMPY_UNIT.megapascal.set_global_relative_scale_factor(SYMPY_UNIT.mega, SYMPY_UNIT.Pa)
SYMPY_UNIT.gigapascal = SYMPY_UNIT.Quantity("gigapascal", abbrev="GPa")
SYMPY_UNIT.gigapascal.set_global_relative_scale_factor(SYMPY_UNIT.giga, SYMPY_UNIT.Pa)
SYMPY_UNIT.kilonewton = SYMPY_UNIT.Quantity("kilonewton", abbrev="kN")
SYMPY_UNIT.kilonewton.set_global_relative_scale_factor(SYMPY_UNIT.kilo, SYMPY_UNIT.N)
SYMPY_UNIT.kilopascal = SYMPY_UNIT.kPa
SYMPY_UNIT.MPa = SYMPY_UNIT.megapascal
SYMPY_UNIT.GPa = SYMPY_UNIT.gigapascal
SYMPY_UNIT.kN = SYMPY_UNIT.kilonewton


class Controller:
    def __init__(self, font_name, font_size, equation_spacing, image_folder_name):
        self.font_name = font_name
        self.font_size = font_size
        self.equation_spacing = equation_spacing
        self.image_folder_name = image_folder_name

    @staticmethod
    def edit_jupyter_css():
        css = "<style> div.output_subarea {padding: 0;}</style>"
        display(HTML(css))

    def create_equation(self, equation_string, convert_to="dimensionless", annotations=None, simplify=False,
                        num_decimal=2, inline=False, eq_font_size_param=None, p_font_size_param=None,
                        s_font_size_param=None):
        # determining font sizes
        eq_font_size = self.font_size if eq_font_size_param is None else eq_font_size_param
        p_font_size = self.font_size if p_font_size_param is None else p_font_size_param
        s_font_size = self.font_size if s_font_size_param is None else s_font_size_param

        eq_obj = Equation(equation_string, convert_to, eq_font_size, inline, num_decimal)
        # Equation
        eq_sympy = eq_obj.compose()
        if eq_sympy is None:
            return
        if simplify:
            eq_sympy = eq_obj.simplify()
            if eq_sympy is None:
                return
        # Space
        space_obj = Space(space=self.equation_spacing)
        space_obj.compose()
        # Annotation
        annot_div = ""
        if annotations:
            ANNOTATIONS.update({str(eq_sympy.lhs): annotations})
            annot_div = "<div style='display: inline-block;'>"
            for i, annot in enumerate(annotations):
                if i == 0:
                    text_obj = Text(annot, font_size=p_font_size, font_name=self.font_name)
                    text_obj.compose()
                else:
                    text_obj = Text(annot, italic=True, font_size=s_font_size, font_name=self.font_name)
                    text_obj.compose()
                annot_div += text_obj.get_html()
            annot_div += "</div>"

        eq_str_lhs = str(eq_sympy.lhs)
        self.add_eq_to_namespace(**{eq_str_lhs: eq_sympy.rhs})
        html = "<div>{equation}{space}{annotations}</div>".format(
            equation=eq_obj.get_html(), space=space_obj.get_html(), annotations=annot_div)
        EQUATION_HISTORY.update({str(eq_sympy.lhs): html})
        display(Markdown(html))
        return eq_sympy.rhs

    def recall_equation(self, lhs):
        html = EQUATION_HISTORY[lhs]
        display(Markdown(html))
        return EQUATION_NAMESPACE[lhs]

    def add_eq_to_namespace(self, **kwargs):
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
        EQUATION_NAMESPACE.update(kwargs)


class Equation:
    def __init__(self, equation_string, convert_to, font_size, inline, num_decimal):
        self.html = ""
        self.num_decimal = num_decimal
        self.equation_string = equation_string
        self.equation_sympy = None
        self.convert_to = convert_to
        self.font_size = font_size
        self.inline = inline
        self.num_decimal = num_decimal

    def compose(self):
        if self.equation_string.count("=") != 1:
            print("Equation must only have 1 equal sign.")
            return None
        left_expr, right_expr = self.equation_string.split("=")
        left_expr = left_expr.strip()
        right_expr = right_expr.strip()

        # check for I, E, S, N, C, O, Q to avoid creating reserved function in sympy.
        left_expr = self.__replace_special_functions(left_expr)
        right_expr = self.__replace_special_functions(right_expr)

        # convert a string equation to a sympy equivalent
        try:
            parse_lhs = parse_expr(left_expr)
            parse_rhs = parse_expr(right_expr)
        except SyntaxError:
            return None

        if len(parse_rhs.atoms(Symbol)) > 0:
            parse_rhs = self.__symbol_to_unit(parse_rhs)
        # convert given string equation to sympy equation.
        self.equation_sympy = Eq(parse_lhs, parse_rhs)
        sym_eq_latex = self.__convert_to_latex(self.equation_sympy)
        html = "<div style='font_size: {font_size}; display: inline-block; vertical-align:top;'>" \
               "$${equation_latex}$$</div>".format(font_size=self.font_size, equation_latex=sym_eq_latex)
        self.set_html(html)
        return self.equation_sympy

    def simplify(self):
        """
            Desc
            ====
            This method will simplify the equation, that is, it will substitute all the variables in the equation
            with their corresponding values previously defined in the equation namespace. It will also simplify the
            final result by using the base unit of its dimension.

            Parameters
            ==========
            rhs_expr:sympy expression - Right hand side expression.

            Returns
            =======
            res_rhs_expr:sympy expression - The resulting expression after evaluation.
        """
        sympy_unit = self.__unit_str_2_unit_sympy(self.convert_to)
        pint_unit = self.__unit_str_2_unit_pint(self.convert_to)
        if sympy_unit is None or pint_unit is None:
            print("Cannot find unit: {}".format(self.convert_to))
            return None
        else:
            rhs_expr = self.equation_sympy.rhs
            if len(rhs_expr.atoms(Symbol)) > 0:
                # get only the needed variables for substitution
                var_list = list(rhs_expr.atoms(Symbol))
                var_sub_dict = {}
                for sym_var in var_list:
                    try:
                        sym_var_str = str(sym_var)
                        var_sub_dict.update({sym_var_str: EQUATION_NAMESPACE[sym_var_str]})
                    except KeyError:
                        pass
                # substitute all variables in the equation
                try:
                    res_rhs_expr = rhs_expr.subs(var_sub_dict).evalf()
                except AttributeError:
                    res_rhs_expr = self.__subs(rhs_expr, var_sub_dict)
            else:
                res_rhs_expr = rhs_expr
            # simplify any special operations ( integral, derivative etc.)
            res_rhs_expr = res_rhs_expr.doit()
            # simplify any unit specific operations
            res_rhs_expr = simplify(res_rhs_expr)
            # as much as possible convert the units in the expression to the units defined.
            if len(res_rhs_expr.atoms(SYMPY_UNIT.Quantity)) == 0:
                res_rhs_expr = res_rhs_expr * sympy_unit
            else:
                res_rhs_expr = SYMPY_UNIT.convert_to(res_rhs_expr, sympy_unit)

            # make output more readable using Pint functions.
            # if magnitude is a number
            if len(res_rhs_expr.atoms(SYMPY_UNIT.Quantity)) == 1 and len(res_rhs_expr.atoms(Number)) == 1:
                if self.convert_to != "dimensionless":
                    # create pint expression
                    pint_expr = PINT_UNIT(str(res_rhs_expr))
                    # simplify pint expression using pint functions
                    # pint_expr = pint_expr.to_compact().to_reduced_units()
                    pint_expr = pint_expr.to_reduced_units()
                    # get magnitude and unit from pint expression
                    mag = pint_expr.magnitude
                    p_unit = pint_expr.units
                    s_unit = self.__unit_pint_2_unit_sympy(p_unit)
                    if s_unit:
                        # create new sympy equation (lhs = magnitude * unit:sympy)
                        res_rhs_expr = mag * s_unit
                    else:
                        return None
        res_rhs_expr = self.__round_expr(res_rhs_expr, self.num_decimal)
        res_eq_sympy = Eq(self.equation_sympy.lhs, res_rhs_expr)
        eq_sympy_latex = self.__convert_to_latex(self.equation_sympy)
        if self.inline:
            res_rhs_latex = self.__convert_to_latex(res_eq_sympy.rhs)
            html = "<div style='font_size:{font_size}; display: inline-block; vertical-align:top;'>" \
                   "$${equation_latex} = {res_rhs_latex}$$</div>".format(font_size=self.font_size,
                                                                         equation_latex=eq_sympy_latex,
                                                                         res_rhs_latex=res_rhs_latex)
        else:
            res_eq_latex = self.__convert_to_latex(res_eq_sympy)
            html = "<div style='font_size:{font_size}; display: inline-block; vertical-align:top;'>" \
                   "<div>$${eq_sympy_latex}$$</div><div>$${res_eq_latex}$$</div></div>".format(
                    font_size=self.font_size, eq_sympy_latex=eq_sympy_latex, res_eq_latex=res_eq_latex)
        self.set_html(html)
        return res_eq_sympy

    def set_html(self, html):
        self.html = html

    def get_html(self):
        return self.html

    def __round_expr(self, expression, num_digits):
        """
            Desc
            ====
            Method for rounding all the number in the equation.

            Parameters
            ==========
            expression:sympy expression - Sympy expression to be rounded off.
            num_digits:int - number of decimal places to be rounded off in each number in the expression.

            Returns
            =======
            sympy expression - expression with rounded Numbers.
        """
        return expression.xreplace({n: round(n, num_digits) for n in expression.atoms(Number)})

    def __subs(self, expr, var_dict):
        expr = parse_expr(str(expr), var_dict)
        expr = self.__symbol_to_unit(expr)
        return expr

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
        new_s = s.xreplace({quan: symbols(str(quan.abbrev)) for quan in s.atoms(SYMPY_UNIT.Quantity)})
        res_latex = "{}".format(latex(new_s, mul_symbol='dot'))
        return res_latex

    def __replace_special_functions(self, expression):
        expr = expression
        rpl = "symbols('{}')"
        reg_pattern = "(?<=[ +\-/*\(\)])[IESNCOQ](?![\w])"
        pattern = regular_expression.compile(reg_pattern)
        match = pattern.search(expression)
        if match:
            match_string = match.group(0)
            expr = pattern.sub(rpl.format(match_string), expression)
        return expr

    def __symbol_to_unit(self, expr):
        # convert symbols to units
        return expr.xreplace(
            {sym: self.__unit_str_2_unit_sympy(str(sym)) for sym in expr.atoms(Symbol)
             if self.__unit_str_2_unit_sympy(str(sym)) and str(sym) not in EQUATION_NAMESPACE})

    def __unit_str_2_unit_pint(self, unit_str):
        try:
            if unit_str == "dimensionless":
                pint_unit = 1
            else:
                pint_unit = PINT_UNIT(unit_str).units
        except UndefinedUnitError:
            pint_unit = None
        return pint_unit

    def __unit_str_2_unit_sympy(self, unit_str):
        unit_sympy = None
        unit_pint = self.__unit_str_2_unit_pint(unit_str)
        if unit_pint:
            unit_sympy = self.__unit_pint_2_unit_sympy(unit_pint)
        return unit_sympy

    def __unit_pint_2_unit_sympy(self, unit_pint):
        unit_str = str(unit_pint)
        if unit_str == "dimensionless":
            unit_sympy = 1
        else:
            try:
                expr_sympy = parse_expr(str(unit_pint))
                unit_sympy = expr_sympy.xreplace({un: eval("SYMPY_UNIT.{}".format(un))
                                                  for un in expr_sympy.atoms(Symbol)})
            except AttributeError:
                unit_sympy = None
        return unit_sympy


class Text:
    def __init__(self, text, bold=False, underline=False, italic=False, text_position="left", font_size=None,
                 font_name=None):
        self.html = ""
        self.text = text
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self.text_position = text_position
        self.font_size = font_size
        self.font_name = font_name

    def compose(self):
        """
            Desc
            ====
            Method that defines Text. Uses HTML to create texts.

            Parameters
            ==========
            text:str - The text you want to display.
            bold:bool - If True, makes the text bold. (text with higher weight)
            underline:bool - If True, adds an underline to the text.
            italic:bool - If True, makes the text italic.
            text_position:str - (left, right, center) position the text to be either at the left, right or center of the
            output screen.

            Returns
            =======
            None
        """
        font_weight = "bold" if self.bold else "normal"
        font_style = "italic" if self.italic else "normal"
        font_decor = "underline" if self.underline else "none"
        html = "<div style='font-family:{font_name}, Arial;font-size:{font_size};" \
               "font-style:{font_style};font-weight:{font_weight};text-decoration:{font_decor};" \
               "text-align:{text_position};'>" \
               "{text}</div>".format(font_name=self.font_name,
                                     font_size=self.font_size,
                                     font_style=font_style,
                                     font_weight=font_weight,
                                     font_decor=font_decor,
                                     text_position=self.text_position,
                                     text=self.text)
        self.set_html(html)

    def get_html(self):
        return self.html

    def set_html(self, html):
        self.html = html


class Space:
    def __init__(self, direction="horizontal", space="0in"):
        self.html = ""
        self.direction = direction
        self.space = space

    def compose(self):
        if self.direction == "horizontal":
            html = "<div style='overflow:hidden;height:1px;width:{space}; display: inline-block;'>" \
                   "</div>".format(space=self.space)
        elif self.direction == "vertical":
            html = "<div style='overflow:hidden;height:{space};width:100%; display: inline-block;'>" \
                   "</div>".format(space=self.space)
        else:
            print("Invalid direction, choose [horizontal or vertical]")
            html = ""
        self.set_html(html)

    def set_html(self, html):
        self.html = html

    def get_html(self):
        return self.html

