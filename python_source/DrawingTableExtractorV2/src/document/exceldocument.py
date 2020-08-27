from src.document.document import Document


class ExcelDocument(Document):
    def __init__(self, excel_doc, filepath):
        self.excel_doc = excel_doc
        self.filepath = filepath

    def create_worksheet(self, worksheet_name):
        return self.excel_doc.create_sheet(worksheet_name)

    def save(self):
        self.excel_doc.save(self.filepath)

    def remove_worksheet(self, worksheet):
        self.excel_doc.remove(worksheet)

    def get_worksheet_by_name(self, name):
        return self.excel_doc[name]
