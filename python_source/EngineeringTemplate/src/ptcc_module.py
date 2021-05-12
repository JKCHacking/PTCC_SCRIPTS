import os
import re as regular_expression
import sympy.physics.units as u
import pint
import random
import matplotlib.pyplot as plt
from sympy import *
from IPython.display import display, Markdown, HTML
from pint.errors import UndefinedUnitError


class CustomDisplay:
    def __init__(self):
        self.writer_output = ""

    def show(self):
        """
            Desc
            ====
            Method for showing all the output of every Writers inside self.args

            Parameters
            ==========
            None

            Returns
            =======
            None
        """
        display(Markdown(self.writer_output))
        self.writer_output = ""

    def hide_toggle(self, for_next=False):
        """
            Desc
            ====
            Method for hiding cell in jupyter notebook

            Parameters
            ==========
            for_next:bool - If True, will hide the next cell of the cell that called this function.
            if False, will hide the cell that called this function.

            Returns
            =======
            Returns the HTML object to be added in the jupyter HTML.
        """
        this_cell = """$('div.cell.code_cell.rendered.selected')"""
        next_cell = this_cell + '.next()'

        toggle_text = 'MODULES INITIALIZATION show/hide'  # text shown on toggle link
        target_cell = this_cell  # target cell to control with toggle
        js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

        if for_next:
            target_cell = next_cell
            toggle_text += ' next cell'
            js_hide_current = this_cell + '.find("div.input").hide();'

        js_f_name = 'code_toggle_{}'.format(str(random.randint(1, 2 ** 64)))

        html = """
            <script>
                function {f_name}() {{
                    {cell_selector}.find('div.input').toggle();
                }}

                {js_hide_current}
            </script>

            <a href="javascript:{f_name}()">{toggle_text}</a>
        """.format(
            f_name=js_f_name,
            cell_selector=target_cell,
            js_hide_current=js_hide_current,
            toggle_text=toggle_text
        )

        return HTML(html)


class EquationWriter:
    def __init__(self, h_space, font_name, font_size, c_display):
        self.h_space = str(h_space) + "in"
        self.font_name = font_name
        self.font_size = str(font_size) + "pt"
        self.equation_namespace = {}
        self.annotations = {}
        self.is_structadeq = True
        self.c_display = c_display

        # initializing units
        self.UNIT = pint.UnitRegistry()
        # setting default unit system
        self.UNIT.default_system = 'SI'  # choices are ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks']

        # define all units that is not supported by Sympy but needed by PTCC
        u.megapascal = u.Quantity("megapascal", abbrev="MPa")
        u.megapascal.set_global_relative_scale_factor(u.mega, u.Pa)
        u.gigapascal = u.Quantity("gigapascal", abbrev="GPa")
        u.gigapascal.set_global_relative_scale_factor(u.giga, u.Pa)
        u.kilonewton = u.Quantity("kilonewton", abbrev="kN")
        u.kilonewton.set_global_relative_scale_factor(u.kilo, u.N)
        u.kilopascal = u.kPa
        u.MPa = u.megapascal
        u.GPa = u.gigapascal
        u.kN = u.kilonewton

    def setup_css(self):
        """
            Desc
            ====
            Method to initialize all custom css for jupyter notebook.

            Parameters
            ==========
            None

            Returns
            =======
            None
        """
        css = "<style>"\
                ".eq_cell {{"\
                    "vertical-align:top;"\
                    "text-align:left;"\
                    "font-family:{font_name}, Arial;"\
                "}}"\
                ".annot_cell {{" \
                    "text-align:left;"\
                    "font-family:{font_name}, Arial;"\
                "}}"\
                ".primary_annot {{" \
                "}}"\
                ".secondary_annot {{" \
                    "font-style: italic;"\
                "}}" \
                ".tbl_eq_row {{" \
                    "display: table-row;" \
                "}}"\
                ".tbl_eq_cell {{" \
                    "display: table-cell;" \
                "}}"\
              "</style>".format(font_name=self.font_name)
        display(HTML(css))

    def conclude(self, component, affirmative):
        """
        Desc
        ====
        This method is used for creating concluding statement. It will generate positive conclusion if there are no
        failed comparison in Compare() method.

        Parameters
        ==========
        component:str - The name of the component to be checked
        affirmative:str - affirmative statement if structurally adequate.

        Return
        ======
        None
        """
        negative = ""
        if not self.is_structadeq:
            negative = "NOT "
        output_string = "<div style='font-family:{font_name}, Arial; font-size:{font_size}'><u><b>THUS, THE " \
                        "{component} IS {negative}{affirmative}</b></u></div>".format(
                            font_name=self.font_name,
                            font_size=self.font_size,
                            component=component.upper(),
                            negative=negative,
                            affirmative=affirmative.upper()
                        )
        self.c_display.writer_output += output_string

    def add_equation(self, **kwargs):
        self.equation_namespace.update(kwargs)

    def assert_components(self, lhs_var_str, rhs_var_str, expected, descr_lhs, descr_rhs, component, statement):
        """
        Desc
        ====
        Function that generates a comparison block.
        Compares computed values to allowable values.

        Parameters
        ==========
        lhs_var_str:str - the left hand side variable.
        rhs_var_str:str - the right hand side variable.
        expected:str - the expected comparison symbol that the two variables should be used to compared. (= , <, >)
        descr_lhs:str - left hand side variable description.
        descr_rhs:str - right hand side variable description.
        component:str - component name to be checked.
        statement:str - the statement if the component is structurally adequate.

        Return
        ======
        None
        """
        try:
            lhs = self.equation_namespace[lhs_var_str]
            rhs = self.equation_namespace[rhs_var_str]
        except KeyError:
            print("Variable does not exists.")
            return

        # check if expression is in the form [N * unit]
        if len(lhs.atoms(Number)) == 1 and len(lhs.atoms(Symbol)) == 2 and len(lhs.atoms(u.Quantity)) == 1 and \
                len(rhs.atoms(Number)) == 1 and len(rhs.atoms(Symbol)) == 2 and len(rhs.atoms(u.Quantity)) == 1:
            operation_word = ""
            actual = ""
            # check if they have the same unit
            lhs_unit = list(lhs.atoms(u.Quantity))[0]
            rhs_unit = list(rhs.atoms(u.Quantity))[0]
            if lhs_unit != rhs_unit:
                lhs = u.convert_to(lhs, rhs_unit)

            mag_lhs = list(lhs.atoms(Number))[0]
            mag_rhs = list(rhs.atoms(Number))[0]
            if mag_lhs < mag_rhs:
                operation_word = "less than"
                actual = "<"
            elif mag_lhs > mag_rhs:
                operation_word = "greater than"
                actual = ">"
            elif mag_lhs == mag_rhs:
                operation_word = "equal to"
                actual = "="

            if expected == actual:
                negative = ""
            else:
                negative = "NOT "
                self.is_structadeq = False

            lhs_latex = self.__convert_to_latex(Eq(parse_expr(lhs_var_str), lhs))
            rhs_latex = self.__convert_to_latex(Eq(parse_expr(rhs_var_str), rhs))
            output_string = "<div style='font-family:{font_name}, Arial; font-size:{font_size}'>Comparing, " \
                            "<div><br>${lhs_expr} {op} {rhs_expr}$</div>" \
                            "<div><br>Since the {descr_lhs} is {operation_word} the {descr_rhs}, <br> <u><b>" \
                            "THE {component} IS {negative}{statement}</u></b></div>" \
                            "</div>".format(
                                lhs_expr=lhs_latex,
                                rhs_expr=rhs_latex,
                                op=actual,
                                descr_lhs=descr_lhs,
                                descr_rhs=descr_rhs,
                                operation_word=operation_word,
                                component=component.upper(),
                                statement=statement.upper(),
                                negative=negative.upper(),
                                font_name=self.font_name,
                                font_size=self.font_size
                            )
            self.c_display.writer_output += output_string
        else:
            print("Expression should be in the form [N * unit] (e.g 3 * mm)")

    def convert(self, var_name, unit_to="", num_decimal=2, print_out=False, inline=False):
        """
        Desc
        ====
        Helper method for converting variable stored in EquationNamespace to the desired unit.
        this method will overwrite the current value of the variable in the EquationNamespace.

        Parameters
        ==========
        var_name:str - variable name in string stored in the EquationNamespace.

        unit_to:str - the unit name that you want to convert to.

        num_decimal:int - number of decimals after conversion.

        print_out:bool - if True, will print the old expression and the new expression after conversion

        inline:bool - if True, will print the new expression inline with the old expression.
        if False, will print in the newline of old expression.

        Return
        ======
        res_expr:sympy expression - the result expression after conversion.
        returns None if:
            * var_name does not exists as key in the EquationNamespace.
            * unit_to is an empty string.
        """
        res_expr = None
        expression = None
        try:
            expression = self.equation_namespace[var_name]
        except KeyError:
            print("Variable does not exists")

        if expression:
            if unit_to == "":
                print("Please input a unit to convert to.")
            else:
                unit_symp = self.__unit_str_2_unit_sympy(unit_to)
                if not unit_symp:
                    print("Cannot find unit {}.".format(unit_to))
                else:
                    res_expr = u.convert_to(expression, unit_symp)
                    res_expr = self.__round_expr(res_expr, num_decimal)
                    # update
                    self.__add_eq_to_namespace(Eq(parse_expr(var_name), res_expr))
        if print_out:
            old_equation = Eq(parse_expr(var_name), expression)
            old_equation_latex = self.__convert_to_latex(old_equation)
            if inline:
                new_expression_latex = self.__convert_to_latex(res_expr)
                out_markdown = "<div style='font-family:{font_name}, Arial;font-size: {font_size};'>" \
                               "${old_eq} = {new_exp}$</div>".format(font_name=self.font_name,
                                                                     font_size=self.font_size,
                                                                     old_eq=old_equation_latex,
                                                                     new_exp=new_expression_latex)
            else:
                new_equation = Eq(parse_expr(var_name), res_expr)
                new_equation_latex = self.__convert_to_latex(new_equation)
                out_markdown = "<div style='font-family:{font_name}, Arial;font-size: {font_size};'>" \
                               "${old_eq}$<br>${new_eq}$</div>".format(font_name=self.font_name,
                                                                       font_size=self.font_size,
                                                                       old_eq=old_equation_latex,
                                                                       new_eq=new_equation_latex)
            self.c_display.writer_output += out_markdown
        return res_expr

    def define(self, equation, unit="dimensionless", annots=None, simplify=False, num_decimal=2,
               inline=False, eq_font_size=None, p_font_size=None, s_font_size=None):
        """
            Desc
            ====
            Interface method for defining and simplifying equations.

            Parameters
            ==========
            equation:str - Equation in string form. example: "y = m * x + b"

            annots:list - List of strings to use for annotating the equation. the first item in the list will be the
            primary annotation and the other items will be the secondary annotations.

            unit:str - Unit to use for the equation. Please check Sympy Documentation for all the supported
            units.

            simplify:bool - If True, the variables in the equation will be substituted by values defined in the
            Equation Namespace and simplify the equation.

            num_decimal:int - number of decimal places to be displayed in the result. This will only work if evaluate
            is True.

            inline:bool - If True, the resulting equation will be in the same line with the original equation.
            If False, the resulting equation will be in the new line from the original equation.
            This will only work if simplify is True.

            eq_font_size:int - font size of the equation.

            p_font_size:int - font size of the primary annotation

            s_font_size:int - font size of the secondary annotations

            Returns
            =======
            None
        """
        # ========================== parsing ===========================
        if equation.count("=") != 1:
            if equation in self.equation_namespace:
                if equation in self.annotations:
                    p_annots = self.annotations[equation][0]
                    s_annots = "<br>".join(self.annotations[equation][1:])
                else:
                    p_annots = ""
                    s_annots = ""

                eq = Eq(parse_expr(equation), self.equation_namespace[equation])
                eq_latex = self.__convert_to_latex(eq)
                out_markdown = self.__create_markdown(eq_latex, self.h_space, p_annots, s_annots)
                self.c_display.writer_output += out_markdown
                return
            else:
                print("You entered an invalid Equation.")
                return

        left_expr, right_expr = equation.split("=")
        left_expr = left_expr.strip()
        right_expr = right_expr.strip()

        # check for I, E, S, N, C, O, Q to avoid creating reserved function in sympy.
        left_expr = self.__replace_special_functions(left_expr)
        right_expr = self.__replace_special_functions(right_expr)

        # convert a string equation to a sympy equivalent
        try:
            parse_lhs = parse_expr(left_expr)
            parse_rhs = parse_expr(right_expr)
            if len(parse_rhs.atoms(Symbol)) > 0:
                parse_rhs = self.__symbol_to_unit(parse_rhs)
            if annots:
                self.__add_annotation(parse_lhs, annots)
        except SyntaxError:
            print("You have entered an invalid equation.")
            return
        # ================= processing and simplifications ==============
        sympy_unit = self.__unit_str_2_unit_sympy(unit)
        if not sympy_unit:
            print("Cannot find unit {}".format(unit))
            return
        if len(parse_rhs.atoms(u.Quantity)) == 0:
            rhs = parse_rhs * sympy_unit
        else:
            rhs = u.convert_to(parse_rhs, sympy_unit)
        sym_eq = Eq(parse_lhs, rhs)
        lhs = rhs
        self.__add_eq_to_namespace(sym_eq)

        if simplify:
            parse_res_rhs = self.__simplify(parse_rhs, unit)
            parse_res_rhs = self.__round_expr(parse_res_rhs, num_decimal)
            res_eq = Eq(parse_lhs, parse_res_rhs)
            self.__add_eq_to_namespace(res_eq)
            lhs = parse_res_rhs
        else:
            res_eq = None
        # ================= display =======================================
        primary_annotation = ""
        secondary_annotations = ""
        if annots:
            primary_annotation = annots[0]
            secondary_annotations = "<br>".join(annots[1:])

        sym_eq_latex = self.__convert_to_latex(sym_eq)
        if simplify:
            if inline:
                res_eq_rhs_latex = self.__convert_to_latex(res_eq.rhs)
                out_latex = "{} = {}".format(sym_eq_latex, res_eq_rhs_latex)
                out_markdown = self.__create_markdown(out_latex,
                                                      self.h_space,
                                                      primary_annotation,
                                                      secondary_annotations,
                                                      eq_font_size,
                                                      p_font_size,
                                                      s_font_size)
            else:
                res_eq_latex = self.__convert_to_latex(res_eq)
                out_markdown = self.__create_markdown(sym_eq_latex,
                                                      self.h_space,
                                                      primary_annotation,
                                                      secondary_annotations,
                                                      eq_font_size,
                                                      p_font_size,
                                                      s_font_size)
                out_markdown += self.__create_markdown(res_eq_latex, self.h_space, eq_font_size=eq_font_size)
        else:
            out_markdown = self.__create_markdown(sym_eq_latex,
                                                  self.h_space,
                                                  primary_annotation,
                                                  secondary_annotations,
                                                  eq_font_size,
                                                  p_font_size,
                                                  s_font_size)
        self.c_display.writer_output += out_markdown
        return lhs

    def __simplify(self, rhs_expr, unit_str):
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
        sympy_unit = self.__unit_str_2_unit_sympy(unit_str)
        pint_unit = self.__unit_str_2_unit_pint(unit_str)
        res_rhs_expr = None
        if sympy_unit is None or pint_unit is None:
            print("Cannot find unit {}".format(unit_str))
        else:
            if len(rhs_expr.atoms(Symbol)) > 0:
                # get only the needed variables for substitution
                var_list = list(rhs_expr.atoms(Symbol))
                var_sub_dict = {}
                for sym_var in var_list:
                    try:
                        sym_var_str = str(sym_var)
                        var_sub_dict.update({sym_var_str: self.equation_namespace[sym_var_str]})
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
            if len(res_rhs_expr.atoms(u.Quantity)) == 0:
                res_rhs_expr = res_rhs_expr * sympy_unit
            else:
                res_rhs_expr = u.convert_to(res_rhs_expr, sympy_unit)

            # make output more readable using Pint functions.
            # if magnitude is a number
            if len(res_rhs_expr.atoms(u.Quantity)) == 1 and len(res_rhs_expr.atoms(Number)) == 1:
                if unit_str != "dimensionless":
                    # create pint expression
                    pint_expr = self.UNIT(str(res_rhs_expr))
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
                        print("Unit {} cannot be found".format(unit_str))
                        res_rhs_expr = None
        return res_rhs_expr

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

    def __subs(self, expr, var_dict):
        expr = parse_expr(str(expr), var_dict)
        expr = self.__symbol_to_unit(expr)
        return expr

    def __symbol_to_unit(self, expr):
        # convert symbols to units
        return expr.xreplace(
            {sym: self.__unit_str_2_unit_sympy(str(sym)) for sym in expr.atoms(Symbol)
             if self.__unit_str_2_unit_sympy(str(sym)) and str(sym) not in self.equation_namespace})

    def __unit_str_2_unit_pint(self, unit_str):
        try:
            if unit_str == "dimensionless":
                pint_unit = 1
            else:
                pint_unit = self.UNIT(unit_str).units
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
                unit_sympy = expr_sympy.xreplace({un: eval("u.{}".format(un))
                                                  for un in expr_sympy.atoms(Symbol)})
            except AttributeError:
                unit_sympy = None
        return unit_sympy

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
        new_s = s.xreplace({quan: symbols(str(quan.abbrev)) for quan in s.atoms(u.Quantity)})
        res_latex = "{}".format(latex(new_s, mul_symbol='dot'))
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

    def __add_annotation(self, lhs, annotation):
        self.annotations.update({str(lhs): annotation})

    def __create_markdown(self, eq_str, hspace="0", primary_annot="", secondary_annot="", eq_font_size=None,
                          p_font_size=None, s_font_size=None):
        """
            Desc
            ====
            Method that creates a markdown for displaying result in jupyter notebook. Uses HTML to create the output.

            Parameters
            ==========
            eq_str:str - Equation string in latex format.

            hspace:str - Measured in Inches, length of the horizontal space between the equation and the
            annotations.

            primary_annot: The primary annotation (annotation inline with the equation).

            secondary_annot: The secondary annotations (annotations under the primary annotation).

            eq_font_size:int - The local font size of the equation. if None, it will use the global font size.

            p_font_size:int - The font size of the primary annotation. if None, it will use the global font size.

            s_font_size:int - The font size of the secondary annotations. if None, it will use the global font size.

            Returns
            =======
            eq_markdown:str - Markdown to be displayed in jupyter notebook.
        """
        if isinstance(eq_font_size, int):
            eq_font_size = str(eq_font_size) + "pt"
        else:
            eq_font_size = self.font_size

        if isinstance(p_font_size, int):
            p_font_size = str(p_font_size) + "pt"
        else:
            p_font_size = self.font_size

        if isinstance(s_font_size, int):
            s_font_size = str(s_font_size) + "pt"
        else:
            s_font_size = self.font_size

        eq_markdown = "<div class='tbl_eq_row'>" \
                      "<div class='tbl_eq_cell eq_cell' style='font-size:{eq_font_size};'>" \
                      "$${eq_str}$$" \
                      "</div>" \
                      "<div class='tbl_eq_cell'>" \
                      "$\\hspace{{{hspace}}}$" \
                      "</div>" \
                      "<div class='tbl_eq_cell annot_cell'>" \
                      "<div class='primary_annot' style='font-size:{p_font_size};'>{p_annot}</div>" \
                      "<div class='secondary_annot' style='font-size:{s_font_size};'>{s_annots}</div>" \
                      "</div>" \
                      "</div>".format(eq_str=eq_str,
                                      hspace=hspace,
                                      p_annot=primary_annot,
                                      s_annots=secondary_annot,
                                      eq_font_size=eq_font_size,
                                      p_font_size=p_font_size,
                                      s_font_size=s_font_size)
        return eq_markdown


class TextWriter:
    def __init__(self, font_name, font_size, c_display):
        self.font_name = font_name
        self.font_size = str(font_size) + "pt"
        self.c_display = c_display

    def define(self, text,  bold=False, underline=False, italic=False, text_position="left", font_size=None):
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
        font_weight = "bold" if bold else "normal"
        font_style = "italic" if italic else "normal"
        font_decor = "underline" if underline else "normal"

        output = self.__create_markdown(text, font_weight, font_style, font_decor,  text_position, font_size)
        self.c_display.writer_output += output

    def create_hspace(self, width):
        """
            Desc
            ====
            Method that display horizontal space.

            Parameters
            ==========
            width:str/int - width of the horizontal space in inches.

            Returns
            =======
            None
        """
        width = str(width)
        hspace_markdown = "<div style='float:left;overflow:hidden;height:1px;width:{width}in;'></div>".format(
            width=width)
        self.c_display.writer_output += hspace_markdown

    def create_vspace(self, height):
        """
            Desc
            ====
            Method that display vertical space.

            Parameters
            ==========
            height:str/int - height of the vertical space in inches.

            Returns
            =======
            None
        """
        height = str(height)
        vspace_markdown = "<div style='float:left;overflow:hidden;height:{height}in;width:100%;'></div>".format(
            height=height)
        self.c_display.writer_output += vspace_markdown

    def __create_markdown(self, text, font_weight, font_style, font_decor, text_position, font_size=None):
        """
            Desc
            ====
            method for creating the markdown (HTML) output of the text writer.

            Parameters
            ==========
            text:str - The text to be displayed.
            font_weight:str - the weight of the font. (Bold, bolder)
            font_style:str - the font style of the text (italic)
            font_decor:str - text modifiers, (underline)
            text_position:str - position of the text to be placed within the output (right, left, center).

            Returns
            =======
            output_markdown:str - Text HTML output
        """
        if isinstance(font_size, int):
            font_size = str(font_size) + "pt"
        else:
            font_size = self.font_size
        output_markdown = ""
        if text_position in ("left", "right", "center"):
            output_markdown = "<div style='font-family:{font_name}, Arial;" \
                                           "font-size:{font_size};" \
                                           "font-style:{font_style};" \
                                           "font-weight:{font_weight};"\
                                           "text-decoration:{font_decor};"\
                                           "text-align:{text_position};'> " \
                              "{text}"\
                              "</div>".format(font_name=self.font_name,
                                              font_size=font_size,
                                              text=text,
                                              font_style=font_style,
                                              font_weight=font_weight,
                                              font_decor=font_decor,
                                              text_position=text_position)
        else:
            print("wrong text position value.")
        return output_markdown


class ImageWriter:
    def __init__(self, image_folder, c_display):
        self.c_display = c_display
        self.output = ""
        self.image_folder = image_folder
        self.img_folder_abs_path = os.path.join(os.getcwd(), image_folder)
        if not os.path.exists(self.img_folder_abs_path):
            print("image folder does not exists.")

    def setup_css(self):
        """
            Desc
            ====
            Method for setting up CSS layouts.

            Parameters
            ==========
            None

            Returns
            =======
            None
        """
        css = "<style>.horizontal {display:inline-block; padding:6px;} .vertical{padding:6px;}" \
              ".template-image {border-width:1px; border-style:solid;}</style>"
        display(HTML(css))

    def define(self, image_names, captions, width=500, height=300, layout="horizontal"):
        """
            Desc
            ====
            Method for defining an Image.

            Parameters
            ==========
            image_names:list of str - The image file path to be displayed.
            captions:str - the caption to be displayed under the image.
            width:str/int - the width of the image in pixels
            height:str/int - the height of the image in pixels
            layout:str (vertical, horizontal) - if there 1 or more images, it will either display the image
            horizontally or vertically.

            Returns
            =======
            None
        """
        output = ""
        if isinstance(image_names, list) and isinstance(captions, list):
            if len(image_names) == len(captions):
                for i, (image_name, caption) in enumerate(zip(image_names, captions)):
                    image_path = os.path.join(self.image_folder, image_name)
                    if os.path.exists(image_path):
                        figure_html = "<figure><img class='template-image' src='{s}' width='{w}px' height='{h}px' " \
                                      "alt='missing jpg'>" \
                                  "<figcaption>{c}</figcaption></figure>".format(
                                    s=image_path,
                                    w=width,
                                    h=height,
                                    c=caption
                                    )
                        if layout == "horizontal":
                            output += "<div class='horizontal'>{}</div>".format(figure_html)
                        elif layout == "vertical":
                            output += "<div class='vertical'>{}</div>".format(figure_html)
                        else:
                            print("Invalid layout!")
                            break
                    else:
                        print("Image {} does not exists".format(image_name))
                self.c_display.writer_output += output
            else:
                print("number of image names and caption names does not match.")
        else:
            print("Please pass a list of image name or list of caption.")


class TableWriter:
    def __init__(self, c_display):
        self.c_display = c_display
        self.table = ""
        self.caption = ""
        self.head = ""
        self.body = ""

    def start(self):
        self.table = "<table>" \
                     "<caption>{caption}</caption>" \
                     "<thead>{head}</thead>" \
                     "<tbody>{body}</tbody>" \
                     "</table>"
        self.caption = ""
        self.head = ""
        self.body = ""

    def end(self):
        self.c_display.writer_output += self.table.format(caption=self.caption, head=self.head, body=self.body)

    def setup_css(self):
        """
            Desc
            ====
            Method that sets up the CSS layouts related to the tables created.

            Parameters
            ==========
            None

            Returns
            =======
            None
        """
        css = "<style> " \
              ".rendered_html td, .rendered_html th {" \
              "text-align:center;}" \
              "</style>"
        display(HTML(css))

    def create_data_cell(self, value, row_span=1, col_span=1):
        """
            Desc
            ====
            Method that creates an HTML based data cell.

            Parameters
            ===========
            value:str - text to be displayed inside the cell
            row_span:str/int - number of rows the cell will merge.
            col_span:str/int - number of columns the cell will merge.

            Returns
            =======
            None
        """
        return "<td rowspan={row_span} colspan={col_span}>{value}</td>".format(value=value,
                                                                               row_span=row_span,
                                                                               col_span=col_span)

    def create_header_cell(self, value, row_span=1, col_span=1):
        """
            Desc
            ====
            Method that creates an HTML based data cell.

            Parameters
            ===========
            value:str - text to be displayed inside the cell
            row_span:str/int - number of rows the cell will merge.
            col_span:str/int - number of columns the cell will merge.

            Returns
            =======
            None
        """
        return "<th rowspan={row_span} colspan={col_span}>{value}</th>".format(value=value,
                                                                               row_span=row_span,
                                                                               col_span=col_span)

    def define_caption(self, caption):
        """
            Desc
            ====
            Method for adding caption

            Parameters
            ==========
            caption:str - text to display in the caption of a table.

            Returns
            =======
            None
        """
        self.caption += caption

    def __create_row(self, cell_list):
        """
            Desc
            ====
            Private method for creating row of a table in HTML.

            Parameters
            ==========
            cell_list:list of string - list of HTML cell strings that returned from data_cell or header_cell methods.

            Returns
            =======
            row:str - HTML cells within HTML row.
        """
        data = ""
        for cell in cell_list:
            data += cell
        row = "<tr>{}</tr>".format(data)
        return row

    def define_column(self, cell_list):
        """
            Desc
            ====
            Method for defining column data. this will update self.head which collects all HTML for a table head.

            Parameters
            ==========
            cell_list:list of string - list of HTML cell strings that returned from data_cell or header_cell methods.

            Returns
            =======
            None
        """
        row = self.__create_row(cell_list)
        self.head += row

    def define_data(self, cell_list):
        """
            Desc
            ====
            Method for defining body data. this will update self.body which collects all HTML for a table body.

            Parameters
            ==========
            cell_list:list of string - list of HTML cell strings that returned from data_cell or header_cell methods.

            Returns
            =======
            None
        """
        row = self.__create_row(cell_list)
        self.body += row


class GraphWriter:
    def __init__(self):
        self.fig = None

    def create_subplots(self, nrows=1, ncolumns=1):
        fig, axs = plt.subplots(nrows, ncolumns)
        self.fig = fig
        return axs

    def create_plot(self, ax, x, y, label="", color="b", marker="", line_style="-"):
        """
        for possible values of color, marker, line_style
        see: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
        """
        ax.plot(x, y, label=label, color=color, marker=marker, linestyle=line_style)

    def set_axis(self, ax, xlabel, ylabel, title, legend=False, grid=False):
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(grid)

        if legend:
            ax.legend()
