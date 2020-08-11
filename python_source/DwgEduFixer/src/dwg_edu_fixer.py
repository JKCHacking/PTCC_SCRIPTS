import argparse
import os
import ctypes
import time
from comtypes import client
from comtypes import COMError
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError

APP_NAME = "BricscadApp.AcadApplication"


class CadDocument:
    def __init__(self):
        try:
            self.cad_application = client.GetActiveObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = False
        except(OSError, COMError):
            self.cad_application = client.CreateObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = False

    def open_document(self, document_path):
        document = None
        if os.path.exists(document_path):
            try:
                self.cad_application.Documents.Open(document_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                print("[ERROR]Invalid Drawing File!: {}".format(document_path))
        return document

    def save_document(self, document_obj):
        if not document_obj.Saved:
            document_obj.Save()

    def save_as_document(self, document_obj, file_name, file_type=None):
        file_type_enum = None
        secu_param = self.cad_application.GetInterfaceObject("BricscadApp.AcadSecurityParams")

        # converts according to the autocad enums
        if file_type == "ac2013_dxf":  # Autocad 2013 DWG
            file_type_enum = 61
        elif file_type == "ac2013_dwg":  # Autocad 2013 DXF
            file_type_enum = 60
        document_obj.SaveAs(file_name, file_type_enum, secu_param)

    def close_all_documents(self):
        self.cad_application.Documents.Close()

    def close_document(self, document_obj):
        document_obj.Close()

    def delete_document(self, document_path):
        os.remove(document_path)


class TrueViewerApp:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.tv_app = None

    def start_app(self):
        tv_exec = "C:\\Program Files\\Autodesk\\DWG TrueView 2020 - English\\dwgviewr.exe"
        self.tv_app = Application(backend='win32').start(tv_exec)
        # self.tv_app.top_window().wait('ready')
        time.sleep(5)

    def show_window(self):
        dlg = self.tv_app.top_window()
        dlg.set_focus()

    def open_file(self, file_full_path):
        print(file_full_path)
        if os.path.exists(file_full_path):
            self.show_window()

            # show the select file window
            str_command = f"%fo"
            send_keys(str_command)
            # wait for the file window to appear
            self.wait_window_by_title('Select File')
            # type the file name
            str_command = f'{file_full_path}~'
            send_keys(str_command, with_spaces=True)
        else:
            print("File not found: {file_full_path}")

    def wait_window_by_title(self, title):
        found = True
        try:
            self.tv_app.window(title_re=title).wait('visible', timeout=5, retry_interval=0.5)
        except TimeoutError:
            print(f"Waiting time expired, Window with title {title} was not found.")
            found = False
        return found

    def get_handle_by_title(self, title):
        handle = 0
        if self.wait_window_by_title(title):
            handle = self.user32.FindWindowW(None, title)
        return handle

    def close_top_window(self):
        send_keys("%{F4}")

    def exit_app(self):
        self.tv_app.kill()


# converts student dwg to dxf then dxf to commercial dwg
def conversion_process(dir_path, orig_fn):
    doc = CadDocument()
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
    # open trueview by executing the dwgviewr.exe
    tv_app = TrueViewerApp()
    tv_app.start_app()

    if os.path.isdir(dir_or_file):
        for dir_path, dir_names, file_names in os.walk(dir_or_file):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(".dwg") and is_student_file(file_full_path, tv_app):
                    conversion_process(dir_path, file_name)
        clean_up_files(dir_or_file)

    elif os.path.isfile(dir_or_file):
        dir_path = os.path.dirname(dir_or_file)
        file_name = os.path.basename(dir_or_file)
        file_full_path = os.path.join(dir_path, file_name)
        if is_student_file(file_full_path, tv_app):
            conversion_process(dir_path, file_name)
            dir = os.path.dirname(dir_or_file)
            clean_up_files(dir)
    tv_app.exit_app()


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
