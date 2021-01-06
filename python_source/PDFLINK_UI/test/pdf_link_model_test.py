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
        model = PDFLinkModel(test_file, "Title1", 1)
        res = model.add_link()
        model.save_document(outfile)
        self.assertEquals(res, OK)

    def test_search_text_002(self):
        '''test case were search algorithm cannot find text'''
        test_file = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.pdf")

        # page must be zero based
        # text to search is not in the pdf file
        model = PDFLinkModel(test_file, "BOOM", 1)
        res = model.add_link()
        self.assertEquals(res, NOT_OK)
