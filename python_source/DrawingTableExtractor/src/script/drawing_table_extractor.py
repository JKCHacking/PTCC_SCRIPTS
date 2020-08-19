import os
from src.factory.applicationfactory import ApplicationFactory
from src.util.exec_timer import timeit
from src.util.constants import Constants
from src.util.logger import get_logger

logger = get_logger("DWGTableExtractor")


def script_process(cadapp, pdfapp, excelapp, drawing_filepath):
    curr_dir = os.path.dirname(drawing_filepath)
    drawing_file_name = os.path.basename(drawing_filepath)
    drawing_name = os.path.splitext(drawing_file_name)[0]

    cad_doc = cadapp.open_document(drawing_filepath)
    workbook = excelapp.create_document()

    layout_names = cad_doc.layouts_to_pdf()
    for layout_name in layout_names:
        pdf_filepath = os.path.join(curr_dir, f'{layout_name}.pdf')
        pdf_doc = pdfapp.create_document(pdf_filepath)
        table_data = pdf_doc.extract_table_data()
        ws = workbook.create_worksheet(layout_name)
        # TODO: Add column names
        for col in range(2, len(table_data.columns) - 1):
            for index in range(2, len(table_data.index) - 1):
                position = (index, col)
                workbook.add_worksheet_contents(ws, table_data[col][index], position)
    excel_output_filepath = os.path.join(curr_dir, f"{drawing_name}.xlsx")
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

    elif os.path.isfile(dir_or_file):
        file_name = os.path.basename(dir_or_file)
        if dir_or_file.endswith(Constants.DWG_FILE_EXT):
            logger.info(f"Working with file: {file_name}")
            script_process(cad_application, pdf_application, excel_application, dir_or_file)

    cad_application.stop_app()
    pdf_application.stop_app()
    excel_application.stop_app()
