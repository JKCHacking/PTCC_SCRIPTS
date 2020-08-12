import os
from src.application.cad_app import CadApp
from src.application.trueview_app import TrueViewerApp
from src.util.constants import Constants
from src.util.logger import get_logger
from src.util.exec_timer import timeit

logger = get_logger("DWGEduFixerLogger")


# converts student dwg to dxf then dxf to commercial dwg
def conversion_process(dir_path, orig_fn, cad_application):
    logger.info("Fixing...")
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
    student_title_dialog = "Student Version - Plot Stamp Detected"
    # open dwg file
    trueview_app.open_file(file_full_path)
    # wait for student version dialog to appear
    is_student = trueview_app.wait_window_by_title(student_title_dialog)
    trueview_app.close_top_window()
    return is_student


def clean_up_files(dir):
    logger.info("Removing unnecessary files...")
    for dir_path, dir_names, file_names in os.walk(dir):
        for file_name in file_names:
            file_full_path = os.path.join(dir_path, file_name)
            if file_full_path.endswith(Constants.BAK_FILE_EXT):
                os.remove(os.path.join(dir_path, file_name))


def write_logfile(str_txt, workdir):
    logfile_fp = os.path.join(workdir, "student_version_list.txt")
    mode = "w"
    if os.path.exists(logfile_fp):
        mode = "a"

    logfile = open(logfile_fp, mode)
    logfile.write(f"{str_txt}\n")
    logfile.close()


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
                logger.info(f"Working with file: {file_name}")
                if file_full_path.endswith(Constants.DWG_FILE_EXT) and is_student_file(file_full_path, tv_app):
                    logger.warning(f"{file_name} is a Student Version")
                    write_logfile(file_name, dir_or_file)
                    # do the conversion "curing" process
                    conversion_process(dir_path, file_name, cad_app)
        clean_up_files(dir_or_file)

    else:
        dir_path = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        logger.info(f"Working with file: {file_name}")
        if dir_or_file.endswith(Constants.DWG_FILE_EXT) and is_student_file(dir_or_file, tv_app):
            logger.info(f"WARNING: {file_name} is a Student Version")
            write_logfile(file_name, dir_path)
            # do the conversion "curing" process
            conversion_process(dir_path, file_name, cad_app)
            clean_up_files(dir_path)
    tv_app.exit_app()
    cad_app.exit_app()