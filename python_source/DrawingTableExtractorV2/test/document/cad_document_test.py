import unittest
import os
from comtypes import client
from comtypes import COMError
from src.document.caddocument import CadDocument
from src.util.constants import Constants
from src.util.util import Utilities


class CadDocumentTest(unittest.TestCase):

    def setUp(self) -> None:
        try:
            self.cad_application = client.GetActiveObject(Constants.BRICS_APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.cad_application = client.CreateObject(Constants.BRICS_APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        handle = Utilities.get_handle_by_title("BricsCAD")
        Utilities.activate_window(handle[0])
        return self.cad_application

    def tearDown(self) -> None:
        self.cad_application.Quit()

    def test_get_layouts(self):
        test_data_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata1.dwg")
        expected = ["Model", "W.01.DL.08A", "W.01.DL.08B", "W.01.DL.08C", "W.01.DL.08D", "W.01.DL.08E"]
        doc = self.cad_application.Documents.Open(test_data_path)
        cad_document = CadDocument(doc)
        layouts = cad_document.get_layouts()
        for layout in layouts:
            self.assertTrue(layout.Name in expected)
        cad_document.close()

    def test_document_fp(self):
        test_data_path = os.path.join(Constants.TEST_DIR, "testdata", "testdata1.dwg")
        expected = test_data_path
        doc = self.cad_application.Documents.Open(test_data_path)
        cad_document = CadDocument(doc)
        self.assertEqual(cad_document.get_document_fp(), expected)
        cad_document.close()
