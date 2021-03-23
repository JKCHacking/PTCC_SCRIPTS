import os
import sympy.physics.units as u
import pint
import random
from sympy import *
from IPython.display import display, Markdown, HTML
from pint.errors import UndefinedUnitError
from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def get_output(self):
        pass

    @abstractmethod
    def set_output(self, output):
        pass


class CustomDisplay:
    def __init__(self, *kwargs):
        self.global_output = ""
        self.args = kwargs

    def show(self):
        for writer in self.args:
            if isinstance(writer, Writer):
                writer_output = writer.get_output()
                if writer_output:
                    self.global_output += writer_output

        display(Markdown(self.global_output))
        self.global_output = ""
        for writer in self.args:
            if isinstance(writer, Writer):
                writer.set_output("")

    def hide_toggle(self, for_next=False):
        this_cell = """$('div.cell.code_cell.rendered.selected')"""
        next_cell = this_cell + '.next()'

        toggle_text = 'Toggle show/hide'  # text shown on toggle link
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


class EquationWriter(Writer):
    def __init__(self, h_space, font_name, font_size):
        self.h_space = str(h_space) + "in"
        self.font_name = font_name
        self.font_size = str(font_size) + "pt"
        self.equation_namespace = {}
        self.output = ""

        self.UNIT = pint.UnitRegistry()
        # setting default unit system
        self.UNIT.default_system = 'SI'  # choices are ['Planck', 'SI', 'US', 'atomic', 'cgs', 'imperial', 'mks']

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
            :return: None
        """
        css = "<style>"\
                ".eq_cell {{"\
                    "vertical-align:top;"\
                    "text-align:left;"\
                    "font-family:{font_name}, Arial;"\
                    "font-size: {font_size};"\
                "}}"\
                ".annot_cell {{" \
                    "text-align:left;"\
                    "font-family:{font_name}, Arial;"\
                "}}"\
                ".primary_annot {{" \
                    "font-size: {font_size};"\
                "}}"\
                ".secondary_annot {{" \
                    "font-size: {font_size};"\
                    "font-style: italic;"\
                "}}" \
                ".tbl_eq_row {{" \
                    "display: table-row;" \
                "}}"\
                ".tbl_eq_cell {{" \
                    "display: table-cell;" \
                "}}"\
              "</style>".format(font_name=self.font_name,
                                font_size=self.font_size)
        display(HTML(css))

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

    def get_output(self):
        """
            Desc
            ====
            Interface method for getting the output of the equation writer.

            Parameters
            =========
            None

            Returns
            =======
            :return: None
        """
        return self.output

    def set_output(self, output):
        """
            Desc
            ====
            Method for setting the output

            Parameters
            ==========
            output:str - string to set for the output

            Returns
            =======
            :return: None
        """
        self.output = output

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
                pint_eq = self.UNIT(str(res_equation.rhs)).to_compact().to_reduced_units()

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
            Method that creates a markdown for displaying result in jupyter notebook. Uses HTML to create the output.

            Parameters
            ==========
            :param eq_str:str - Equation string in latex format.
            :param hspace:str - Measured in Inches, length of the horizontal space between the equation and the
            annotations.
            :param primary_annot: The primary annotation (annotation inline with the equation).
            :param secondary_annot: The secondary annotations (annotations under the primary annotation).

            Returns
            =======
            :return: eq_markdown:str - Markdown to be displayed in jupyter notebook.
        """
        eq_markdown = "<div class='tbl_eq_row'>" \
                      "<div class='tbl_eq_cell eq_cell'>" \
                      "${eq_str}$" \
                      "</div>" \
                      "<div class='tbl_eq_cell'>" \
                      "$\\hspace{{{hspace}}}$" \
                      "</div>" \
                      "<div class='tbl_eq_cell annot_cell'>" \
                      "<div class='primary_annot'>{p_annot}</div>" \
                      "<div class='secondary_annot'>{s_annots}</div>" \
                      "</div>" \
                      "</div>".format(eq_str=eq_str,
                                      hspace=hspace,
                                      p_annot=primary_annot,
                                      s_annots=secondary_annot)
        return eq_markdown


class TextWriter(Writer):
    def __init__(self, font_name, font_size):
        self.font_name = font_name
        self.font_size = str(font_size) + "pt"
        self.output = ""

    def define(self, text,  bold=False, underline=False, italic=False, text_position="left"):
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

        output = self.__create_markdown(text, font_weight, font_style, font_decor,  text_position)
        self.output += output

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
        self.output += hspace_markdown

    def create_vspace(self, height):
        """
            Desc
            ====
            Method that display vertical space.

            Parameters
            ==========
            width:str/int - width of the vertical space in inches.

            Returns
            =======
            None
        """
        height = str(height)
        vspace_markdown = "<div style='float:left;overflow:hidden;height:{height}in;width:100%;'></div>".format(
            height=height)
        self.output += vspace_markdown

    def __create_markdown(self, text, font_weight, font_style, font_decor, text_position):
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
        None
        """
        output_markdown = ""
        if text_position in ("left", "right", "center"):
            output_markdown = "<div style='font-family:{font_name}, Arial; " \
                                           "font-size:{font_size}; " \
                                           "font-style:{font_style};" \
                                           "font-weight:{font_weight};"\
                                           "text-decoration:{font_decor};"\
                                           "text-align:{text_position};'> " \
                              "{text}"\
                              "</div>".format(font_name=self.font_name,
                                              font_size=self.font_size,
                                              text=text,
                                              font_style=font_style,
                                              font_weight=font_weight,
                                              font_decor=font_decor,
                                              text_position=text_position)
        else:
            print("wrong text position value.")
        return output_markdown

    def get_output(self):
        """
            Desc
            ====
            Interface method for getting the output of the text writer.

            Parameters
            =========
            None

            Returns
            =======
            None
        """
        return self.output

    def set_output(self, output):
        """
            Desc
            ====
            Interface method for setting the output of the text writer

            Parameters
            ==========
            output:str - string to set to the output.

            Returns
            =======
            None
        """
        self.output = output


class ImageWriter(Writer):
    def __init__(self, image_folder):
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
        css = "<style>.horizontal {display:inline-block; padding-right:6px} .vertical{padding-bottom:6px;}</style>"
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
                        figure_html = "<figure><img src='{s}' width='{w}px' height='{h}px' alt='missing jpg'>" \
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
                self.output += output
            else:
                print("number of image names and caption names does not match.")
        else:
            print("Please pass a list of image name or list of caption.")

    def get_output(self):
        """
            Desc
            ====
            Interface method for getting the output of the Image writer.

            Parameters
            =========
            None

            Returns
            =======
            None
        """
        return self.output

    def set_output(self, output):
        """
            Desc
            ====
            Interface method for setting the output of the Image writer

            Parameters
            ==========
            output:str - string to set to the output.

            Returns
            =======
            None
        """
        self.output = output


class TableWriter(Writer):
    def __init__(self):
        self.output = ""
        self.table = "<table>" \
                      "<caption>{caption}</caption>" \
                      "<thead>{head}</thead>" \
                      "<tbody>{body}</tbody>" \
                      "</table>"
        self.caption = ""
        self.head = ""
        self.body = ""

    def setup_css(self):
        css = "<style> " \
              ".rendered_html td, .rendered_html th {" \
              "text-align:center;}" \
              "</style>"
        display(HTML(css))

    def data_cell(self, value, row_span=1, col_span=1):
        return "<td rowspan={row_span} colspan={col_span}>{value}</td>".format(value=value,
                                                                               row_span=row_span,
                                                                               col_span=col_span)

    def header_cell(self, value, row_span=1, col_span=1):
        return "<th rowspan={row_span} colspan={col_span}>{value}</th>".format(value=value,
                                                                               row_span=row_span,
                                                                               col_span=col_span)

    def define_caption(self, caption):
        self.caption += caption

    def __create_row(self, cell_list):
        data = ""
        for cell in cell_list:
            data += cell
        row = "<tr>{}</tr>".format(data)
        return row

    def define_column(self, cell_list):
        row = self.__create_row(cell_list)
        self.head += row

    def define_data(self, cell_list):
        row = self.__create_row(cell_list)
        self.body += row

    def get_output(self):
        self.output = self.table.format(caption=self.caption, head=self.head, body=self.body)
        return self.output

    def set_output(self, output):
        self.output = output
        self.table = "<table>" \
                     "<caption>{caption}</caption>" \
                     "<thead>{head}</thead>" \
                     "<tbody>{body}</tbody>" \
                     "</table>"
        self.caption = output
        self.head = output
        self.body = output


class GraphWriter:
    def setup(self):
        pass

    def write(self):
        pass

