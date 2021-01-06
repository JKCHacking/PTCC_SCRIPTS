import os
import unittest
from src.pdf_link_model import PDFLinkModel
from src.util.constants import Constants


OK = 1
NOT_OK = -1


class PDFLinkModelTest(unittest.TestCase):

    def test_search_text_001(self):
        '''
            testing normal case
        '''
        test_file = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.pdf")
        outfile = os.path.join(Constants.TEST_DIR, "testdata", "testdata001_modified.pdf")

        # page must be zero based
        model = PDFLinkModel(test_file)
        res = model.add_link("Title1", 1)
        model.save_document(outfile)
        self.assertEqual(res, OK)

    def test_search_text_002(self):
        '''test case were search algorithm cannot find text'''
        test_file = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.pdf")

        # page must be zero based
        # text to search is not in the pdf file
        model = PDFLinkModel(test_file)
        res = model.add_link("BOOM", 1)
        self.assertEqual(res, NOT_OK)

    def test_get_total_num_page_001(self):
        test_file = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.pdf")

        model = PDFLinkModel(test_file)
        count = model.get_total_num_page()
        self.assertEqual(count, 3)
