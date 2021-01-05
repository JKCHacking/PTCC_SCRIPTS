import os
import unittest
from src.pdf_link_model import PDFLinkModel
from src.util.constants import Constants


class PDFLinkModelTest(unittest.TestCase):
    def test_search_text_001(self):
        test_file = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.pdf")
        outfile = os.path.join(Constants.TEST_DIR, "testdata", "testdata001_modified.pdf")

        # page must be zero based
        model = PDFLinkModel(test_file, "Title1", 1)
        model.add_link()
        model.save_document(outfile)
