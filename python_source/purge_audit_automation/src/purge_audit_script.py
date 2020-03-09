#!usr/bin/env python

#################################
# Author: Joshnee Kim B. Cunanan
# last Modified: 02 Feb 2020
# Version: 3.0
#################################

from comtypes import client
from comtypes import COMError
from shutil import copyfile
from logger import Logger
import os

# This still works since Bricscad is also an Autocad Application.
# This will make the script universal for both application.
BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
AUTOCAD_APP_NAME = "AutoCAD.Application"
APP_NAME = BRICSCAD_APP_NAME  # switch to other app CAD here.

DRAWING_EXTENSION = ".dwg"
BAK_FILES = ".bak"
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
logger = Logger()


class PurgeAuditScript:
    def __init__(self, directory):
        self.logger = logger.get_logger()
        try:
            self.cad_application = client.GetActiveObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{APP_NAME} is not Running...")
            self.logger.info(f"Opening {APP_NAME}...")
            self.cad_application = client.CreateObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True

        self.script_directory = directory
        self.root_directory = os.path.dirname(self.script_directory)
        self.input_directory = os.path.join(self.root_directory, "input")
        self.output_directory = os.path.join(self.root_directory, "output")
        self.error_directory = os.path.join(self.output_directory, "error")
        self.cant_open = []
        self.wrong_tab_name = []
        self.total_files = 0

    def begin_automation(self):
        self._traverse_in_directory(self.input_directory)
        self.clean_up_files(self.input_directory)
        self.logger.warning("There are {} Error Files found!".format(len(self.cant_open) + len(self.wrong_tab_name)))
        self.create_summary_log()

    def _traverse_in_directory(self, directory):
        if len(os.listdir(directory)) == 0:
            self.logger.warning(f"The {os.path.basename(directory)} Folder is empty...")
        else:
            for dir_path, dir_names, file_names in os.walk(directory):
                for file_name in file_names:
                    file_full_path = os.path.join(dir_path, file_name)
                    if file_full_path.endswith(DRAWING_EXTENSION):
                        self.make_changes_to_drawing(file_full_path)
                        self.total_files = self.total_files + 1

    def make_changes_to_drawing(self, drawing_full_path):
        file_name = os.path.basename(drawing_full_path)
        document = self._open_file(drawing_full_path)
        if document is not None:
            self.__purge_document(document, file_name)
            self.__audit_document(document, file_name)
            has_wrong_tab = self._apply_standards(document, file_name)
            if has_wrong_tab:
                self.wrong_tab_name.append(drawing_full_path)

            self._save_document(document, file_name)
            self.copy_file(drawing_full_path, has_error=has_wrong_tab)

        else:
            self.cant_open.append(drawing_full_path)
            self.copy_file(drawing_full_path, has_error=True)

    def _open_file(self, drawing_full_path):
        self.logger.info("Opening File: {}".format(drawing_full_path))
        document = None
        if os.path.exists(drawing_full_path):
            try:
                self.cad_application.Documents.Open(drawing_full_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                self.logger.error("[ERROR]Invalid Drawing File!: {}".format(drawing_full_path))
        return document

    def __purge_document(self, document, file_name):
        if document:
            for i in range(0, 5):
                self.logger.info("[ATTEMPT{}]Purging Drawing: {}...".format(i+1, file_name))
                document.PurgeAll()
        self.logger.info("Purging Drawing Done...")

    def __audit_document(self, document, file_name):
        self.logger.info("Auditing Drawing: {}...".format(file_name))
        if document:
            document.AuditInfo(True)
        self.logger.info("Auditing Drawing Done...")

    def _apply_standards(self, document, file_name, fix=False):
        self.logger.info("Setting to Paper Space with zoom extent..")

        file_name = file_name.split(".")[0]
        file_name_list = file_name.split("-")
        document_counter_len = file_name_list[len(file_name_list) - 1]  # gets the last element in the list.
        counter_digit_num = len(document_counter_len)
        post_fix_count = "0000"

        if document_counter_len.isdigit():
            post_fix_count = file_name_list.pop()

        post_fix_count_int = int(post_fix_count)
        has_wrong_tab = False

        layouts = document.Layouts
        layout_num = layouts.Count

        correct_layout_dict = {}

        for layout in layouts:
            current_layout_name = layout.Name

            document.ActiveLayout = layout
            self.cad_application.ZoomExtents()
            # command_str = "._ZOOM\nextents\n"
            # document.SendCommand(command_str)
            document.SetVariable("TREEDEPTH",
                                 document.GetVariable("TREEDEPTH"))

            post_fix_count_str = str(post_fix_count_int).zfill(counter_digit_num)
            post_fix_count_str = "" if int(post_fix_count_str) == 0 else post_fix_count_str
            prefix_file_name = "-".join(file_name_list)
            expected_layout_name = "-".join([prefix_file_name, post_fix_count_str])

            if current_layout_name != "Model":
                if current_layout_name != expected_layout_name:
                    has_wrong_tab = True
                    if fix:
                        correct_layout_dict[current_layout_name] = expected_layout_name
                post_fix_count_int = post_fix_count_int + 1

        error_count = 0
        if fix:
            while error_count < (layout_num - 1):
                for layout in layouts:
                    if layout.Name != "Model":
                        current_l_name = layout.Name
                        try:
                            layout.Name = correct_layout_dict[current_l_name]
                        except KeyError:
                            self.logger.warning("Layout List changed!")
                            error_count = error_count + 1

        for i in range(0, layout_num):
            layout = layouts[i]
            if layout.Name != "Model":
                document.ActiveLayout = layout
                break

        return has_wrong_tab

    def _save_document(self, document, file_name):
        self.logger.info("Saving changes to Drawing: {}".format(file_name))
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def copy_file(self, drawing_full_path, has_error=False):
        file_relative_path = drawing_full_path.replace(self.input_directory + os.sep, "")
        file_directory = os.path.dirname(file_relative_path)
        file_directory = os.path.normpath(file_directory)
        path_list = file_directory.split(os.sep)

        file_name = os.path.basename(drawing_full_path)

        if not has_error:
            # save the file in output directory with all its prerequisite directories
            self.create_file_hierarchy(path_list)
            file_path_to_output = os.path.join(self.output_directory, file_relative_path)
            try:
                copyfile(drawing_full_path, file_path_to_output)
            except FileExistsError:
                self.logger.warning("File {} already exists!".format(os.path.basename(drawing_full_path)))
        elif has_error:
            wrong_tab_name_dir = os.path.join(self.error_directory, "wrong_tab_name")
            cant_open_dir = os.path.join(self.error_directory, "cant_open")
            other = os.path.join(self.error_directory, "other")

            if drawing_full_path in self.cant_open:
                file_path_to_output = os.path.join(cant_open_dir, file_name)
            elif drawing_full_path in self.wrong_tab_name:
                file_path_to_output = os.path.join(wrong_tab_name_dir, file_name)
            else:
                file_path_to_output = os.path.join(other, file_name)

            os.makedirs(self.error_directory, exist_ok=True)
            os.makedirs(other, exist_ok=True)
            os.makedirs(wrong_tab_name_dir, exist_ok=True)
            os.makedirs(cant_open_dir, exist_ok=True)

            try:
                copyfile(drawing_full_path, file_path_to_output)
            except FileExistsError:
                self.logger.warning("File {} already exists!".format(file_name))

    def create_file_hierarchy(self, path_list):
        self.logger.info("Creating file hierarchy with path list: {}".format(path_list))
        compiled_directory = self.output_directory
        try:
            # create folders
            for directory in path_list:
                if directory != "":
                    compiled_directory = os.path.join(compiled_directory, directory)
                    os.makedirs(compiled_directory, exist_ok=True)

        except FileExistsError:
            self.logger.warning("Directory already exists.")
        self.logger.info("Creating file hierarchy done.")

    def clean_up_files(self, directory):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(directory):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))
        self.logger.info("Cleaning up files done..")

    def create_summary_log(self):
        log_file_path = os.path.join(self.output_directory, "log.txt")
        log_file = open(log_file_path, "w")
        total_errors_found = len(self.cant_open) + len(self.wrong_tab_name)
        total_no_errors = self.total_files - total_errors_found

        log_file.write("=============SUMMARY===============\n")
        log_file.write(f"Total Number of Drawings: {self.total_files}\n")
        log_file.write(f"Total Drawings with no Errors: {total_no_errors}\n")
        log_file.write(f"Total Drawings with Errors: {total_errors_found}\n")
        log_file.write(f"\t{len(self.cant_open)} files can't be opened.\n")
        log_file.write(f"\t{len(self.wrong_tab_name)} files with inconsistent layout and file name.\n")
        log_file.close()


if __name__ == "__main__":
    purge_audit_object = PurgeAuditScript(DIRECTORY)
    purge_audit_object.begin_automation()
