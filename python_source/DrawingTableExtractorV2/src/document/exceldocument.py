from src.document.document import Document
from src.util.logger import get_logger

logger = get_logger("ExcelDocumentLogger")


class ExcelDocument(Document):
    def __init__(self, excel_doc, filepath):
        self.excel_doc = excel_doc
        self.filepath = filepath

    def create_worksheet(self, worksheet_name):
        return self.excel_doc.create_sheet(worksheet_name)

    def save(self):
        logger.info(f"Excel file saved here: {self.filepath}")
        self.excel_doc.save(self.filepath)

    def remove_worksheet(self, worksheet):
        self.excel_doc.remove(worksheet)

    def get_worksheet_by_name(self, name):
        return self.excel_doc[name]

    def get_worksheets(self):
        return self.excel_doc.worksheets
