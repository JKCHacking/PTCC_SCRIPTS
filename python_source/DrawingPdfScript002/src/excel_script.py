from src.excel_script_meta import ExcelScriptMeta
from openpyxl import Workbook


class ExcelScript(metaclass=ExcelScriptMeta):
    def __init__(self, output_fp):
        self.workbook = Workbook()
        self.output = output_fp

    def create_worksheet(self, title):
        worksheet = self.workbook.create_sheet(title)
        return worksheet

    def setup_worksheet(self, worksheet, columns_list):
        

    def add_contents(self, contents):
        pass