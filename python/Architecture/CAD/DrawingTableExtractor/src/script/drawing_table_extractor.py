import os
from src.factory.applicationfactory import ApplicationFactory
from src.util.exec_timer import timeit
from src.util.constants import Constants
from src.util.logger import get_logger
from src.util.util import Utilities

logger = get_logger("DWGTableExtractor")


def add_table_column(ws, wb):
    wb.add_worksheet_contents(ws, "NO.", (1, 1))
    wb.add_worksheet_contents(ws, "DRAWING NUMBER", (1, 2))
    wb.add_worksheet_contents(ws, "DRAWING TITLE", (1, 3))
    wb.add_worksheet_contents(ws, "SUBMISSION 1", (1, 4))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 4))
    wb.add_worksheet_contents(ws, "DATE", (2, 5))
    wb.add_worksheet_contents(ws, "SUBMISSION 2", (1, 6))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 6))
    wb.add_worksheet_contents(ws, "DATE", (2, 7))
    wb.add_worksheet_contents(ws, "SUBMISSION 3", (1, 8))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 8))
    wb.add_worksheet_contents(ws, "DATE", (2, 9))
    wb.add_worksheet_contents(ws, "SUBMISSION 4", (1, 10))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 10))
    wb.add_worksheet_contents(ws, "DATE", (2, 11))
    wb.add_worksheet_contents(ws, "SUBMISSION 5", (1, 12))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 12))
    wb.add_worksheet_contents(ws, "DATE", (2, 13))
    wb.add_worksheet_contents(ws, "SUBMISSION 6", (1, 14))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 14))
    wb.add_worksheet_contents(ws, "DATE", (2, 15))
    wb.add_worksheet_contents(ws, "SUBMISSION 7", (1, 16))
    wb.add_worksheet_contents(ws, "REV. NO", (2, 16))
    wb.add_worksheet_contents(ws, "DATE", (2, 17))


def script_process(cadapp, pdfapp, excelapp, drawing_filepath):
    curr_dir = os.path.dirname(drawing_filepath)
    drawing_file_name = os.path.basename(drawing_filepath)
    drawing_name = os.path.splitext(drawing_file_name)[0]

    cad_doc = cadapp.open_document(drawing_filepath)
    workbook = excelapp.create_document("")

    layout_names = cad_doc.layouts_to_pdf()
    for layout_name in layout_names:
        pdf_filepath = os.path.join(curr_dir, f'{layout_name}.pdf')
        pdf_doc = pdfapp.create_document(pdf_filepath)
        table_data = pdf_doc.extract_table_data()
        ws = workbook.create_worksheet(layout_name)
        add_table_column(ws, workbook)
        for index in range(3, len(table_data.index) - 1):
            column = 6
            for col in range(2, len(table_data.columns) - 1):
                value = table_data[col][index]
                if value:
                    value_list = value.split("\n")
                    len_value = len(value_list)
                    if len_value == 3:
                        drawing_title = value_list[0]
                        rev_no = ""
                        date = ""
                        for value in value_list:
                            if Utilities.is_date(value):
                                date = value
                            elif len(value) > len(drawing_title):
                                drawing_title = value
                            else:
                                rev_no = value
                        pos_dwg_title = (index, 3)
                        workbook.add_worksheet_contents(ws, drawing_title, pos_dwg_title)
                        pos_rev_no = (index, 4)
                        workbook.add_worksheet_contents(ws, rev_no, pos_rev_no)
                        pos_date = (index, 5)
                        workbook.add_worksheet_contents(ws, date, pos_date)
                    elif len_value == 2:
                        # other submission
                        rev_no = value_list[0]
                        date = value_list[1]
                        if Utilities.is_date(value_list[0]):
                            rev_no = value_list[1]
                            date = value_list[0]
                        workbook.add_worksheet_contents(ws, rev_no, (index, column))
                        workbook.add_worksheet_contents(ws, date, (index, column + 1))
                        column += 2
                    else:
                        position = (index, col - 1)
                        workbook.add_worksheet_contents(ws, value, position)
    cad_doc.close()
    excel_output_filepath = os.path.join(curr_dir, f"{drawing_name}.xlsx")
    default_ws = workbook.get_worksheet_by_name("Sheet")
    workbook.remove_worksheet(default_ws)
    workbook.save(excel_output_filepath)


@timeit
def main(dir_or_file):
    cad_application = ApplicationFactory.create_application("CadApp")
    pdf_application = ApplicationFactory.create_application("PdfApp")
    excel_application = ApplicationFactory.create_application("ExcelApp")

    cad_application.start_app()
    pdf_application.start_app()
    excel_application.start_app()

    if os.path.isdir(dir_or_file):
        for dir_path, dir_names, file_names in os.walk(dir_or_file):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DWG_FILE_EXT):
                    logger.info(f"Working with file: {file_name}")
                    script_process(cad_application, pdf_application, excel_application, file_full_path)
        Utilities.clean_up_file(['.pdf', '.bak'], dir_or_file)
    elif os.path.isfile(dir_or_file):
        directory = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        if dir_or_file.endswith(Constants.DWG_FILE_EXT):
            logger.info(f"Working with file: {file_name}")
            script_process(cad_application, pdf_application, excel_application, dir_or_file)
        Utilities.clean_up_file(['.pdf', '.bak'], directory)
    cad_application.stop_app()
    pdf_application.stop_app()
    excel_application.stop_app()
