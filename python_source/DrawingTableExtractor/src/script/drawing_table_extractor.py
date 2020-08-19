import os
from src.factory.applicationfactory import ApplicationFactory
from src.util.exec_timer import timeit
from src.util.constants import Constants
from src.util.logger import get_logger

logger = get_logger("DWGTableExtractor")


def script_process():
    pass


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
                    pass

    elif os.path.isfile(dir_or_file):
        file_name = os.path.basename(dir_or_file)
        logger.info(f"Working with file: {file_name}")
        if dir_or_file.endswith(Constants.DWG_FILE_EXT):
            pass

    cad_application.stop_app()
    pdf_application.stop_app()
    excel_application.stop_app()
