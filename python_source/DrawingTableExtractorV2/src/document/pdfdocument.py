import camelot
from src.document.document import Document


class PdfDocument(Document):
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_table_data(self):
        tables = camelot.read_pdf(self.filepath)
        return tables[0].df
