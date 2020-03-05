#!usr/bin/env python

#################################
# Author: Joshnee Kim B. Cunanan
# last Modified: 02 Feb 2020
# Version: 1.0
#################################

from comtypes import client
from comtypes import COMError
from shutil import copyfile
from logger import Logger
import os

# This still works since Bricscad is also an Autocad Application.
# This will make the script universal for both application.
# BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
AUTOCAD_APP_NAME = "AutoCAD.Application"
DRAWING_EXTENSION = ".dwg"
BAK_FILES = ".bak"
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
logger = Logger()


class PurgeAuditScript:
    def __init__(self, directory):
        self.logger = logger.get_logger()
        try:
            self.cad_application = client.GetActiveObject(AUTOCAD_APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{AUTOCAD_APP_NAME} is not Running...")
            self.logger.info(f"Opening {AUTOCAD_APP_NAME}...")
            self.cad_application = client.CreateObject(AUTOCAD_APP_NAME, dynamic=True)
            self.cad_application.Visible = True

        self.script_directory = directory
        self.root_directory = os.path.dirname(self.script_directory)
        self.input_directory = os.path.join(self.root_directory, "input")
        self.output_directory = os.path.join(self.root_directory, "output")
        self.error_directory = os.path.join(self.output_directory, "error")
        self.err_num = 0

    def begin_automation(self):
        self.err_num = 0
        self.__traverse_in_directory()
        self.clean_up_files()
        self.logger.warning("There are {} Error Files found!".format(self.err_num))
        self.cad_application.Visible = False

    def __traverse_in_directory(self):
        if len(os.listdir(self.input_directory)) == 0:
            self.logger.warning("Input Folder is empty...")
        else:
            for dir_path, dir_names, file_names in os.walk(self.input_directory):
                for file_name in file_names:
                    file_full_path = os.path.join(dir_path, file_name)
                    if file_full_path.endswith(DRAWING_EXTENSION):
                        self.make_changes_to_drawing(file_full_path)

    def make_changes_to_drawing(self, drawing_full_path):
        file_name = os.path.basename(drawing_full_path)
        document = self.__open_file(drawing_full_path)
        if document is not None:
            self.__purge_document(document, file_name)
            self.__audit_document(document, file_name)
            self.__set_paper_layout_zoom_extent(document)
            self.__save_document(document, file_name)
            self.copy_file_with_extension(drawing_full_path)
        else:
            self.copy_file_with_extension(drawing_full_path, has_error=True)
            self.err_num = self.err_num + 1

    def __open_file(self, drawing_full_path):
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

    def __set_paper_layout_zoom_extent(self, document):
        self.logger.info("Setting to Paper Space with zoom extent..")
        # enum:
        # acModelSpace = 1
        # acPaperSpace = 2
        document.ActiveSpace = 1
        # layout_count = document.Layouts.Count
        for layout in document.Layouts:
            document.ActiveLayout = layout
            self.cad_application.ZoomExtents()
        document.ActiveLayout = document.Layouts[0]

    def __save_document(self, document, file_name):
        self.logger.info("Saving changes to Drawing: {}".format(file_name))
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def copy_file_with_extension(self, drawing_full_path, has_error=False):
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
            file_path_to_output = os.path.join(self.error_directory, file_name)

            try:
                os.mkdir(self.error_directory)
            except FileExistsError:
                self.logger.info("Error directory already exists")

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

    def clean_up_files(self):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(self.input_directory):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))
        self.logger.info("Cleaning up files done..")


if __name__ == "__main__":
    purge_audit_object = PurgeAuditScript(DIRECTORY)
    purge_audit_object.begin_automation()
