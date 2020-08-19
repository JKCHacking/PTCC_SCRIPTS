from src.document.document import Document


class ExcelDocument(Document):
    def __init__(self, excel_doc):
        self.excel_doc = excel_doc

    def create_worksheet(self, worksheet_name):
        pass

    def add_worksheet_contents(self, worksheet, contents, position):
        row = position[0]
        col = position[1]
        worksheet.cell(row=row, column=col, value=contents)

    def save(self, filepath):
        self.excel_doc.save(filepath)
