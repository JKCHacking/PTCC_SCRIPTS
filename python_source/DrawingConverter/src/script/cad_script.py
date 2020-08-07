import os
from comtypes import client
from comtypes import COMError
from src.constants import Constants
from src.logger import Logger
from src.script import Script

logger = Logger()


class CadScript(Script):
    def __init__(self, cad_application):
        self.cad_application = cad_application
        self.logger = logger.get_logger()

    def __str__(self):
        return "CadScript Object"

    def open_file(self, drawing_full_path):
        self.logger.info(f"Opening File: {drawing_full_path}")

        document = None
        if os.path.exists(drawing_full_path):
            try:
                self.cad_application.Documents.Open(drawing_full_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                self.logger.error("[ERROR]Invalid Drawing File!: {}".format(drawing_full_path))
        return document

    def save_file(self, document):
        self.logger.info(f"Saving document input.dwg")
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def delete_file(self, doc):
        pass

    def check_file(self, doc):
        pass

    def dwg2dxf(self, document):
        pass

    def dxf2dwg(self, document):
        pass