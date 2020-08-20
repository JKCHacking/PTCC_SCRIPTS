from src.document.document import Document


class ExcelDocument(Document):
    def __init__(self, excel_doc):
        self.excel_doc = excel_doc

    def create_worksheet(self, worksheet_name):
        return self.excel_doc.create_sheet(worksheet_name)

    def add_worksheet_contents(self, worksheet, contents, position):
        row = position[0]
        col = position[1]
        worksheet.cell(row=row, column=col, value=contents)

    def save(self, filepath):
        self.excel_doc.save(filepath)

    def remove_worksheet(self, worksheet):
        self.excel_doc.remove(worksheet)

    def get_worksheet_by_name(self, name):
        return self.excel_doc[name]