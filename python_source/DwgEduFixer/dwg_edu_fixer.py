import argparse
import os
from src.application.cad_app import CadApp
from src.application.trueview_app import TrueViewerApp
from src.document.cad_document import CadDocument


# converts student dwg to dxf then dxf to commercial dwg
def conversion_process(dir_path, orig_fn, cad_application):
    doc = CadDocument(cad_application.get_cad_application())
    file_name = os.path.splitext(orig_fn)[0]

    dwg_fp = os.path.join(dir_path, f"{file_name}.dwg")
    dxf_fp = os.path.join(dir_path, f"{file_name}.dxf")

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
            if file_full_path.endswith(".bak"):
                os.remove(os.path.join(dir_path, file_name))


def main(dir_or_file):
    cad_app = CadApp()
    cad_app.start_app()

    tv_app = TrueViewerApp()
    tv_app.start_app()

    if os.path.isdir(dir_or_file):
        for dir_path, dir_names, file_names in os.walk(dir_or_file):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(".dwg") and is_student_file(file_full_path, tv_app):
                    conversion_process(dir_path, file_name, cad_app)
        clean_up_files(dir_or_file)

    elif os.path.isfile(dir_or_file):
        dir_path = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        file_full_path = os.path.join(dir_path, file_name)
        if is_student_file(file_full_path, tv_app):
            conversion_process(dir_path, file_name, cad_app)
            dir = os.path.dirname(dir_or_file)
            clean_up_files(dir)
    tv_app.exit_app()
    cad_app.exit_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("--in_file", help="Input DWG File", type=str)
    parser.add_argument('--in_folder', help="Input DWG Folder", type=str)
    args = parser.parse_args()

    if args.in_file and os.path.isfile(args.in_file):
        main(args.in_file)
    elif args.in_folder and os.path.isdir(args.in_folder):
        main(args.in_folder)
    else:
        print("Invalid input, please check your input commands.")
