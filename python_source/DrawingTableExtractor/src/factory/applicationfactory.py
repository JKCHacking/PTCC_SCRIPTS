from src.application.excelapp import ExcelApp
from src.application.pdfapp import PdfApp
from src.application.cadapp import CadApp


class ApplicationFactory:

    @staticmethod
    def create_application(application_name):
        if application_name == "CadApp":
            return CadApp()
        elif application_name == "PdfApp":
            return PdfApp()
        elif application_name == "ExcelApp":
            return ExcelApp()
