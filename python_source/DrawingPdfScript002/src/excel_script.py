from src.excel_script_meta import ExcelScriptMeta
from openpyxl import Workbook


class ExcelScript(metaclass=ExcelScriptMeta):
    def __init__(self, output_fp):
        self.workbook = Workbook()
        self.output = output_fp

        # remove default worksheet created
        def_ws = self.workbook.get_sheet_by_name("Sheet")
        self.workbook.remove(def_ws)

    def create_worksheet(self, title):
        worksheet = self.workbook.create_sheet(title)
        return worksheet

    def setup_worksheet(self, worksheet, columns_list):
        # for now, creates necessary columns for each commenter.
        for i, col in enumerate(columns_list):
            worksheet.cell(row=1, column=i+1, value=col)

    def add_worksheet_contents(self, worksheet, contents, position, overwrite=True):
        row = position[0]
        col = position[1]
        # prevents from overwriting current contents
        if not overwrite:
            curr_content = worksheet.cell(row=row, column=col)
            if curr_content != " " or curr_content != "":
                row = row + 1
        worksheet.cell(row=row, column=col, value=contents)
    
    def save_workbook(self):
        self.workbook.save(self.output)

    def delete_worksheet(self, worksheet):
        self.workbook.remove(worksheet)
