import unittest
import os
from src.document.pdfdocument import PdfDocument
from src.util.constants import Constants


class PdfDocumentTest(unittest.TestCase):

    def test_extract_table_data(self):
        test_filepath = os.path.join(Constants.TEST_DIR, "testdata", "testdata2.pdf")
        expected = "01.COVER"

        pdf_doc = PdfDocument(test_filepath)
        data = pdf_doc.extract_table_data()
        actual = data[3][3]
        self.assertEquals(actual, expected)
