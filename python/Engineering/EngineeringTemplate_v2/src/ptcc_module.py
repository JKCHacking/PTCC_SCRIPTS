import os
import re as regular_expression
import sympy.physics.units as SYMPY_UNIT
import pint
from IPython.display import display, Markdown, HTML
from sympy import *
from pint.errors import UndefinedUnitError
from abc import ABC, abstractmethod

EQUATION_NAMESPACE = {}
ANNOTATIONS = {}

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
        self.is_adequate = True
        self.output = OutputContainer()

    @staticmethod
    def edit_jupyter_css():
        css = "<style> div.output_subarea {padding: 0; overflow-x: clip;}</style>"
        display(HTML(css))

    def create_equation(self, input_equation, convert_to="dimensionless", annotations=None, simplify=False,
                        num_decimal=2, inline=False, eq_font_size_param=None, p_font_size_param=None,
                        s_font_size_param=None):
        # determining font sizes
        eq_font_size = self.font_size if eq_font_size_param is None else eq_font_size_param
        p_font_size = self.font_size if p_font_size_param is None else p_font_size_param
        s_font_size = self.font_size if s_font_size_param is None else s_font_size_param
        # Equation
        eq_obj = Equation(input_equation, eq_font_size)
        if simplify:
            eq_obj.simplify(convert_to, inline, num_decimal)
        if eq_obj.equation is None:
            return
        else:
            self.add_eq_to_namespace(**{str(eq_obj.equation.lhs): eq_obj})
        # Space
        space_obj = Space("horizontal", space=self.equation_spacing)
        # Annotation
        annotation_group = TextGroup()
        if annotations:
            ANNOTATIONS.update({str(eq_obj.equation.lhs): annotations})
            for i, annot in enumerate(annotations):
                if i == 0:
                    text_obj = Text(annot, bold=False, underline=False, italic=False, font_size=p_font_size,
                                    font_name=self.font_name)
                else:
                    text_obj = Text(annot, bold=False, underline=False, italic=True, font_size=s_font_size,
                                    font_name=self.font_name)
                annotation_group.add(text_obj)
        equation_row = EquationRow()
        equation_row.add(eq_obj)
        equation_row.add(space_obj)
        equation_row.add(annotation_group)
        self.output.add(equation_row)
        return eq_obj.equation.rhs

    def create_text(self, text_string, bold=False, underline=False, italic=False,
                    font_size=None, font_name=None):
        font_size = self.font_size if font_size is None else font_size
        font_name = self.font_name if font_name is None else font_name
        text_obj = Text(text_string, bold, underline, italic, font_size, font_name)
        self.output.add(text_obj)

    def create_vertical_space(self, space):
        space_obj = Space("vertical", space)
        self.output.add(space_obj)

    def create_horizontal_space(self, space):
        space_obj = Space("horizontal", space)
        self.output.add(space_obj)

    def create_line_break(self):
        line_br_obj = LineBreak()
        self.output.add(line_br_obj)

    def create_header(self, text_string, font_size=None, font_name=None):
        font_size = self.font_size if font_size is None else font_size
        font_name = self.font_name if font_name is None else font_name
        line_break_obj = LineBreak()

        text_obj = Text(text_string, bold=True, underline=True, italic=False, font_size=font_size, font_name=font_name)
        self.output.add(text_obj)
        self.output.add(line_break_obj)

    def create_title(self, section, main_title, references, project_name_location, font_size=None, font_name=None):
        font_size = self.font_size if font_size is None else font_size
        font_name = self.font_name if font_name is None else font_name
        line_break_obj = LineBreak()

        section_obj = Text(section, bold=True, underline=False, italic=False, font_size=font_size, font_name=font_name)
        self.output.add(section_obj)
        self.output.add(line_break_obj)
        self.output.add(line_break_obj)
        main_title_obj = Text(main_title, bold=True, underline=True, italic=False, font_size=font_size,
                              font_name=font_name)
        self.output.add(main_title_obj)
        self.output.add(line_break_obj)
        for reference in references:
            ref_obj = Text(reference, bold=False, underline=False, italic=False, font_size=font_size,
                           font_name=font_name)
            self.output.add(ref_obj)
        self.output.add(line_break_obj)
        proj_name_loc_obj = Text(project_name_location, bold=False, underline=False, italic=False, font_size=font_size,
                                 font_name=font_name)
        self.output.add(proj_name_loc_obj)
        self.output.add(line_break_obj)

    def create_table(self, data_table, caption):
        table = HTMLTable(caption)
        for table_row in data_table:
            tbl_row = TableRow()
            for data_dict in table_row:
                data = data_dict["data"]
                colspan = data_dict["colspan"] if "colspan" in data_dict and isinstance(data_dict["colspan"], int)\
                    else 1
                rowspan = data_dict["rowspan"] if "rowspan" in data_dict and isinstance(data_dict["rowspan"], int)\
                    else 1
                cell = HTMLCell(data, rowspan=rowspan, colspan=colspan)
                tbl_row.add(cell)
            table.add(tbl_row)
        self.output.add(table)

    def create_image(self, images, captions, layout="horizontal", width="500px", height="300px"):
        if isinstance(images, list) and isinstance(captions, list):
            if len(images) == len(captions):
                if os.path.exists(os.path.join("", self.image_folder_name)):
                    image_group = ImageGroup(layout)
                    for image_name, caption in zip(images, captions):
                        image_path = os.path.join(self.image_folder_name, image_name)
                        if os.path.exists(image_path):
                            image_obj = HTMLImage(image_path, caption, width, height)
                            image_group.add(image_obj)
                        else:
                            print("Image does not exists", image_name)
                    self.output.add(image_group)
                else:
                    print("Image folder does not exists")
            else:
                print("Number of images and caption must be equal.")
        else:
            print("Please pass a list of image name or list of caption.")

    def create_graph(self):
        pass

    def recall_equation(self, lhs):
        equation_obj = EQUATION_NAMESPACE[lhs]
        try:
            annotations = ANNOTATIONS[lhs]
        except KeyError:
            annotations = []
        res = self.create_equation(equation_obj.equation, annotations=annotations)
        return res

    def convert(self, lhs, unit_to="", num_decimal=2, printout=False, inline=False):
        eq_obj = EQUATION_NAMESPACE[lhs]
        # create a new object to avoid side effects
        new_eq_obj = Equation(eq_obj.equation, eq_obj.font_size)
        new_eq_obj.convert(unit_to, inline=inline, decimal=num_decimal)
        if new_eq_obj.equation is None:
            return
        else:
            self.add_eq_to_namespace(**{str(new_eq_obj.equation.lhs): new_eq_obj})
        if printout:
            self.output.add(new_eq_obj)
        return new_eq_obj.equation.rhs

    def compare(self, var1, var2, operation, desc_var1, desc_var2, component, conclusion):
        try:
            eq_var1 = EQUATION_NAMESPACE[var1]
            eq_var2 = EQUATION_NAMESPACE[var2]
        except KeyError as ke:
            print(str(ke))
            return None

        lhs = eq_var1.equation.rhs
        rhs = eq_var2.equation.rhs

        compared = simplify(lhs - rhs)

        operation_word = ""
        operation_symbol = ""

        try:
            if compared == 0:
                operation_word = "equal"
                operation_symbol = "="
            elif compared < 0:
                operation_word = "less than"
                operation_symbol = "<"
            elif compared > 0:
                operation_word = "greater than"
                operation_symbol = ">"
        except TypeError:
            print("One of the expressions has unknown variables")
            return None

        if operation == operation_symbol:
            negative = ""
        else:
            negative = "NOT "
            self.is_adequate = False

        line_break = LineBreak()
        comparison_block = ComparisonBlock()
        comparison_block.add(Text("Comparing,", False, False, False, self.font_size, self.font_name))
        comparison_block.add(line_break)
        comparison_block.add(line_break)
        comparison_block.add(eq_var1)
        comparison_block.add(Space("horizontal", self.font_size))
        comparison_block.add(Text(operation_symbol, True, False, True, self.font_size, self.font_name))
        comparison_block.add(Space("horizontal", self.font_size))
        comparison_block.add(eq_var2)
        comparison_block.add(line_break)
        comparison_block.add(Text("Since the {desc_var1} is {operation_word} the {desc_var2}".format(
            desc_var1=desc_var1, desc_var2=desc_var2, operation_word=operation_word),
            False, False, False, self.font_size, self.font_name))
        comparison_block.add(line_break)
        comparison_block.add(Text("THE {component} IS {negative}{conclusion}".format(component=component.upper(),
                                                                                     negative=negative,
                                                                                     conclusion=conclusion.upper()),
                                  True, True, False, self.font_size, self.font_name))
        self.output.add(comparison_block)

    def conclude(self, component, affirmative):
        negative = ""
        if not self.is_adequate:
            negative = "NOT "
        conclusion_obj = Text("THUS, THE {component} IS {negative}{affirmative}".format(
            component=component.upper(), negative=negative, affirmative=affirmative.upper()),
            bold=True, underline=True, italic=False, font_size=self.font_size, font_name=self.font_name)
        self.output.add(conclusion_obj)

    def display_output(self, alignment="left"):
        self.output.set_alignment(alignment)
        html = self.output.get_html()
        # display html
        display(Markdown(html))
        # create new instance to clear the contents
        self.output = OutputContainer()

    def add_eq_to_namespace(self, **kwargs):
        """
        :param kwargs:
        MUl, Pow, Add, String, Equation Object
        :return:
        """
        lhs = list(kwargs.keys())[0]
        equation_input = kwargs[lhs]
        if not isinstance(equation_input, Equation):
            if isinstance(equation_input, str):
                equation = "{} = {}".format(lhs, equation_input)
            elif isinstance(equation_input, (Mul, Add, Pow)):
                equation = Eq(parse_expr(lhs), equation_input)
            else:
                equation = None
            eq_obj = Equation(equation, font_size=self.font_size)
        else:
            eq_obj = equation_input
        eq_dict = {lhs: eq_obj}
        EQUATION_NAMESPACE.update(eq_dict)

# =========================================COMPONENT CLASSES=========================================================


class Component(ABC):
    pass


class Leaf(Component):
    def __init__(self):
        self.html = ""

    def get_html(self):
        return self.html

    def set_html(self, html):
        self.html = html

    @abstractmethod
    def compose(self):
        pass


class Composite(Component):
    def __init__(self):
        self.html = ""
        self.components = []

    def add(self, comp_obj):
        self.components.append(comp_obj)

    def remove(self, comp_obj):
        pass

    def set_html(self, html):
        self.html = html

    @abstractmethod
    def get_html(self):
        pass


class Equation(Leaf):
    def __init__(self, input_equation, font_size):
        super().__init__()
        self.input_equation = input_equation
        self.equation = None
        self.font_size = font_size
        self.compose()

    def compose(self):
        if isinstance(self.input_equation, str):
            if self.input_equation.count("=") != 1:
                print("Equation must only have 1 equal sign.")
                return None
            left_expr, right_expr = self.input_equation.split("=")
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
                print("You have entered an invalid expression.")
                return None

            if len(parse_rhs.atoms(Symbol)) > 0:
                parse_rhs = self.__symbol_to_unit(parse_rhs)
            # convert given string equation to sympy equation.
            self.equation = Eq(parse_lhs, parse_rhs)
        elif isinstance(self.input_equation, Equality):
            self.equation = self.input_equation
        else:
            print("Invalid equation")
            return None
        sym_eq_latex = self.__convert_to_latex(self.equation)
        html = "<div style='font_size: {font_size}; display: inline-block; vertical-align:top;'>" \
               "$${equation_latex}$$</div>".format(font_size=self.font_size, equation_latex=sym_eq_latex)
        self.set_html(html)

    def simplify(self, convert_to, inline, num_decimal):
        """
            Desc
            ====
            This method will simplify the equation, that is, it will substitute all the variables in the equation
            with their corresponding values previously defined in the equation namespace. It will also simplify the
            final result by using the base unit of its dimension.

            Parameters
            ==========
            convert_to
            inline

            Returns
            =======
            res_rhs_expr:sympy expression - The resulting expression after evaluation.
        """
        old_equation = self.equation
        sympy_unit = self.__unit_str_2_unit_sympy(convert_to)
        pint_unit = self.__unit_str_2_unit_pint(convert_to)
        if sympy_unit is None or pint_unit is None:
            print("Cannot find unit: {}".format(convert_to))
            return None
        else:
            rhs_expr = old_equation.rhs
            if len(rhs_expr.atoms(Symbol)) > 0:
                # get only the needed variables for substitution
                var_list = list(rhs_expr.atoms(Symbol))
                var_sub_dict = {}
                for sym_var in var_list:
                    try:
                        sym_var_str = str(sym_var)
                        var_sub_dict.update({sym_var_str: EQUATION_NAMESPACE[sym_var_str].equation.rhs})
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
                if convert_to != "dimensionless":
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
        res_rhs_expr = self.__round_expr(res_rhs_expr, num_decimal)
        res_eq_sympy = Eq(old_equation.lhs, res_rhs_expr)
        eq_sympy_latex = self.__convert_to_latex(old_equation)
        if inline:
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
        self.equation = res_eq_sympy

    def convert(self, unit_to, decimal, inline):
        self.simplify(unit_to, inline, decimal)

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


class Text(Leaf):
    def __init__(self, text, bold, underline, italic, font_size, font_name):
        super().__init__()
        self.text = text
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self.font_size = font_size
        self.font_name = font_name
        self.compose()

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
               "display: inline-block;'>" \
               "{text}</div>".format(font_name=self.font_name,
                                     font_size=self.font_size,
                                     font_style=font_style,
                                     font_weight=font_weight,
                                     font_decor=font_decor,
                                     text=self.text)
        self.set_html(html)


class Space(Leaf):
    def __init__(self, direction, space):
        super().__init__()
        self.direction = direction
        self.space = space
        self.compose()

    def compose(self):
        if self.direction == "horizontal":
            html = "<div float:left; style='overflow:hidden;height:1px;width:{space}; display: inline-block;'>" \
                   "</div>".format(space=self.space)
        elif self.direction == "vertical":
            html = "<div style='overflow:hidden;height:{space};width:100%;'>" \
                   "</div>".format(space=self.space)
        else:
            print("Invalid direction, choose [horizontal or vertical]")
            html = ""
        self.set_html(html)


class LineBreak(Leaf):
    def __init__(self):
        super().__init__()
        self.html = ""
        self.compose()

    def compose(self):
        html = "<br>"
        self.set_html(html)


class HTMLImage(Leaf):
    def __init__(self, image_path, caption, width, height):
        super().__init__()
        self.html = ""
        self.image_path = image_path
        self.caption = caption
        self.width = width
        self.height = height
        self.compose()

    def compose(self):
        html = "<figure style='display: inline-block; padding:6px;'>" \
               "<img style='border-width: 1px; border-style: solid;' src='{source}' width='{width}' height='{height}' "\
               "alt='missing jpg'>" \
               "<figcaption>{caption}</figcaption>" \
               "</figure>".format(source=self.image_path,
                                  width=self.width,
                                  height=self.height,
                                  caption=self.caption)
        self.set_html(html)


class HTMLCell(Leaf):
    def __init__(self, data, rowspan, colspan):
        super().__init__()
        self.data = data
        self.rowspan = rowspan
        self.colspan = colspan
        self.compose()

    def compose(self):
        html = "<td rowspan={rowspan} colspan={colspan} style='text-align: center;" \
               " background: #ffffff; border-top-width: 1px; border-top-style: solid;" \
               " border-bottom-width: 1px; border-bottom-style: solid;'>{data}</td>".format(rowspan=self.rowspan,
                                                                                            colspan=self.colspan,
                                                                                            data=self.data)
        self.set_html(html)


class TableRow(Composite):
    def __init__(self):
        super().__init__()

    def get_html(self):
        html = "<tr>{inner_html}</tr>"
        inner_html = ""
        for cell in self.components:
            inner_html += cell.get_html()
        self.set_html(html.format(inner_html=inner_html))
        return self.html


class HTMLTable(Composite):
    def __init__(self, caption):
        super().__init__()
        self.caption = caption

    def get_html(self):
        html = "<table><caption style='text-align: center; color: black; font-weight: bold;'>{caption}</caption>" \
               "<tbody>{inner_html}</tbody></table>"
        inner_html = ""
        for row in self.components:
            inner_html += row.get_html()
        self.set_html(html.format(caption=self.caption, inner_html=inner_html))
        return self.html


class ImageGroup(Composite):

    def __init__(self, layout):
        super().__init__()
        self.layout = layout

    def get_html(self):
        if self.layout == "horizontal":
            newline = ""
        else:
            newline = "<br>"

        html = "<div style='display: inline-block;'>{inner_html}</div>"
        inner_html = ""
        for image_obj in self.components:
            inner_html += image_obj.get_html() + newline
        self.set_html(html.format(inner_html=inner_html))
        return self.html


class TextGroup(Composite):
    def __init__(self):
        super().__init__()

    def get_html(self):
        html = "<div style='display: inline-block;'>{inner_html}</div>"
        inner_html = ""
        for annotation_obj in self.components:
            inner_html += annotation_obj.get_html() + "<br>"
        self.set_html(html.format(inner_html=inner_html))
        return self.html


class EquationRow(Composite):
    def __init__(self):
        super().__init__()

    def get_html(self):
        html = "<div>{inner_html}</div>"
        inner_html = ""
        for comp_obj in self.components:
            inner_html += comp_obj.get_html()
        self.set_html(html.format(inner_html=inner_html))
        return self.html


class ComparisonBlock(Composite):
    def __init__(self):
        super().__init__()

    def get_html(self):
        html = "<div>{inner_html}</div>"
        inner_html = ""
        for comp_obj in self.components:
            inner_html += comp_obj.get_html()
        self.set_html(html.format(inner_html=inner_html))
        return self.html


class OutputContainer(Composite):
    def __init__(self):
        super().__init__()
        self.alignment = ""

    def get_html(self):
        html = "<div style='text-align: {alignment};'>{inner_html}</div>"
        inner_html = ""
        for comp_obj in self.components:
            inner_html += comp_obj.get_html()
        return html.format(inner_html=inner_html, alignment=self.alignment)

    def set_alignment(self, alignment):
        self.alignment = alignment
