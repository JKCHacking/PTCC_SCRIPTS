#!/usr/bin/env python
from comtypes import client
from comtypes import COMError
from src.constants import Constants
from src.logger import Logger
import os

logger = Logger()


class CadScript:

    def __init__(self):
        self.logger = logger.get_logger()
        try:
            self.cad_application = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{Constants.APP_NAME} is not Running...")
            self.logger.info(f"Opening {Constants.APP_NAME}...")
            self.cad_application = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.cad_application.Visible = True

    def clean_up_files(self):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(Constants.OUTPUT_DIR):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))

    def save_document(self, document):
        self.logger.info(f"Saving document input.dwg")
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

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

    @staticmethod
    def get_modelspace(document):
        return document.ModelSpace

    @staticmethod
    def get_paperspace(document):
        return document.PaperSpace
