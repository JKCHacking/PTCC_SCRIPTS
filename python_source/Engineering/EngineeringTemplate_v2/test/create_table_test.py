import unittest
from src.ptcc_module import Controller


class CreateTableTest(unittest.TestCase):
    def test_create_table_001(self):
        EQUATION_ANNOTATION_SPACE = "2in"
        FONT_NAME = "Times New Roman"
        FONT_SIZE = "12pt"
        IMAGE_FOLDER_NAME = "images"
        controller = Controller(FONT_NAME, FONT_SIZE, EQUATION_ANNOTATION_SPACE, IMAGE_FOLDER_NAME)
        table_data = [
            [{"data": "column1"}, {"data": "column2"}],
            [{"data": "row1col1"}, {"data": "row1col2"}],
            [{"data": "row2col1"}, {"data": "row2col2"}],
        ]
        expected = "<div style='text-align: ;'><table><caption style='text-align: center; color: black; " \
                   "font-weight: bold;'></caption>" \
                   "<tbody><tr><td rowspan=1 colspan=1 style='text-align: center; background: #ffffff; " \
                   "border-top-width: 1px; border-top-style: solid; border-bottom-width: 1px; " \
                   "border-bottom-style: solid;'>column1</td><td rowspan=1 colspan=1 style='text-align: center; " \
                   "background: #ffffff; border-top-width: 1px; border-top-style: solid; border-bottom-width: 1px; " \
                   "border-bottom-style: solid;'>column2</td></tr><tr>" \
                   "<td rowspan=1 colspan=1 style='text-align: center; background: #ffffff; border-top-width: 1px;" \
                   " border-top-style: solid; border-bottom-width: 1px; border-bottom-style: solid;'>row1col1</td>" \
                   "<td rowspan=1 colspan=1 style='text-align: center; background: #ffffff; border-top-width: 1px; " \
                   "border-top-style: solid; border-bottom-width: 1px; border-bottom-style: solid;'>row1col2</td></tr>" \
                   "<tr><td rowspan=1 colspan=1 style='text-align: center; background: #ffffff; border-top-width: 1px; " \
                   "border-top-style: solid; border-bottom-width: 1px; border-bottom-style: solid;'>row2col1</td>" \
                   "<td rowspan=1 colspan=1 style='text-align: center; background: #ffffff; border-top-width: 1px; " \
                   "border-top-style: solid; border-bottom-width: 1px; border-bottom-style: solid;'>row2col2</td></tr>" \
                   "</tbody></table></div>"
        controller.create_table(table_data, caption="")
        self.assertEqual(expected, controller.output.get_html())
