import os
from src.application.cad_app import CadApp
from src.application.trueview_app import TrueViewerApp
from src.util.constants import Constants
from src.util.logger import get_logger
from src.util.exec_timer import timeit

main_logger = get_logger("MainLogger")


# converts student dwg to dxf then dxf to commercial dwg
def conversion_process(dir_path, orig_fn, cad_application):
    main_logger.info("Fixing...")
    doc = cad_application.create_document()
    # getting file name without extension
    file_name = os.path.splitext(orig_fn)[0]

    dwg_fp = os.path.join(dir_path, f"{file_name}{Constants.DWG_FILE_EXT}")
    dxf_fp = os.path.join(dir_path, f"{file_name}{Constants.DXF_FILE_EXT}")

    # convert dwg to dxf
    document_obj = doc.open_document(dwg_fp)
    doc.save_as_document(document_obj=document_obj, file_name=dxf_fp, file_type="ac2013_dxf")
    doc.close_document(document_obj)

    # convert dxf to dwg
    document_obj = doc.open_document(dxf_fp)
    doc.save_as_document(document_obj=document_obj, file_name=dwg_fp, file_type="ac2013_dwg")
    doc.close_document(document_obj)

    doc.delete_document(dxf_fp)


def is_student_file(file_full_path, trueview_app):
    error_title_dialog = "Student Version - Plot Stamp Detected"
    # open dwg file
    trueview_app.open_file(file_full_path)
    # check if dialog error is displayed
    is_student = trueview_app.wait_window_by_title(error_title_dialog)
    trueview_app.close_top_window()
    return is_student


def clean_up_files(dir):
    for dir_path, dir_names, file_names in os.walk(dir):
        for file_name in file_names:
            file_full_path = os.path.join(dir_path, file_name)
            if file_full_path.endswith(Constants.BAK_FILE_EXT):
                os.remove(os.path.join(dir_path, file_name))


@timeit
def main(dir_or_file):
    cad_app = CadApp()
    cad_app.start_app()

    tv_app = TrueViewerApp()
    tv_app.start_app()

    if os.path.isdir(dir_or_file):
        for dir_path, dir_names, file_names in os.walk(dir_or_file):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                main_logger.info(f"Working with file: {file_name}")
                if file_full_path.endswith(Constants.DWG_FILE_EXT):
                    # file is a student version file
                    if is_student_file(file_full_path, tv_app):
                        main_logger.warning(f"{file_name} is a Student Version")
                        # do the conversion "curing" process
                        conversion_process(dir_path, file_name, cad_app)
                    else:
                        # go to the next file
                        pass

        clean_up_files(dir_or_file)

    elif os.path.isfile(dir_or_file):
        dir_path = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        main_logger.info(f"Working with file: {file_name}")
        if dir_or_file.endswith(Constants.DWG_FILE_EXT) and is_student_file(dir_or_file, tv_app):
            main_logger.info(f"WARNING: {file_name} is a Student Version")
            conversion_process(dir_path, file_name, cad_app)
            clean_up_files(dir_path)
    tv_app.exit_app()
    cad_app.exit_app()