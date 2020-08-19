from openpyxl import Workbook
from src.application.application import Application
from src.document.exceldocument import ExcelDocument


class ExcelApp(Application):
    def start_app(self):
        pass

    def stop_app(self):
        pass

    def open_document(self, filepath):
        pass

    def create_document(self, filepath):
        workbook = Workbook()
        return ExcelDocument(workbook)
