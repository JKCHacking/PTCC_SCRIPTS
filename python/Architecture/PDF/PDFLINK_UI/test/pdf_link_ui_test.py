import unittest
from src.pdf_link_ui import PDFLinkUI


class PDFLinkUITest(unittest.TestCase):
    def test_get_widget_by_name_001(self):
        '''test for finding widget using objectname'''

        ui = PDFLinkUI()
