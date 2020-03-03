#!usr/bin/env python

from comtypes import client
from comtypes import COMError
from shutil import copyfile
import os

BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
DRAWING_EXTENSION = ".dwg"
BAK_FILES = ".bak"
DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class PurgeAuditScript:
    def __init__(self, directory):
        try:
            self.bricscad_application = client.GetActiveObject(BRICSCAD_APP_NAME, dynamic=True)
        except(OSError, COMError):
            print("Bricscad is not Running...")
            print("Opening Bricscad...")
            self.bricscad_application = client.CreateObject(BRICSCAD_APP_NAME, dynamic=True)
            self.bricscad_application.Visible = True

        self.script_directory = directory
        self.root_directory = os.path.dirname(self.script_directory)
        self.input_directory = os.path.join(self.root_directory, "input")
        self.output_directory = os.path.join(self.root_directory, "output")
        self.error_directory = os.path.join(self.output_directory, "error")

    def begin_automation(self):
        self.__traverse_in_directory()

    def __traverse_in_directory(self):
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
            self.__save_document(document, file_name)
            self.copy_file_with_extension(drawing_full_path)
        else:
            self.copy_file_with_extension(drawing_full_path, has_error=True)

    def __open_file(self, drawing_full_path):
        print("Opening File: {}".format(drawing_full_path))
        document = None
        if os.path.exists(drawing_full_path):
            try:
                self.bricscad_application.Documents.Open(drawing_full_path)
                document = self.bricscad_application.ActiveDocument
            except COMError:
                print("[ERROR]Invalid Drawing File!: {}".format(drawing_full_path))
        return document

    def __purge_document(self, document, file_name):
        if document:
            for i in range(0, 5):
                print("[ATTEMPT{}]Purging Drawing: {}...".format(i+1, file_name))
                document.PurgeAll()
        print("Purging Drawing Done...")

    def __audit_document(self, document, file_name):
        print("Auditing Drawing: {}...".format(file_name))
        if document:
            document.AuditInfo(True)
        print("Auditing Drawing Done...")

    def __save_document(self, document, file_name):
        print("Saving changes to Drawing: {}".format(file_name))
        if not document.Saved:
            print("There are unsaved changes in the Drawing")
            document.Save()
            self.bricscad_application.Documents.Close()
        print("Saving done and Closed...")

    def copy_file_with_extension(self, drawing_full_path, has_error=False):
        file_relative_path = drawing_full_path.replace(self.input_directory + os.sep, "")
        file_relative_path = os.path.normpath(file_relative_path)

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
                print("File {} already exists!".format(os.path.basename(drawing_full_path)))
        elif has_error:
            file_path_to_output = os.path.join(self.error_directory, file_name)
            try:
                copyfile(drawing_full_path, file_path_to_output)
            except FileExistsError:
                print("File {} already exists!".format(file_name))

    def create_file_hierarchy(self, path_list):
        try:
            # create folders
            for directory in path_list:
                if directory != "":
                    directory_str = os.path.join(self.output_directory, directory)
                    file_heirarchy_directory = os.path.join(self.output_directory, directory_str)
                    os.makedirs(file_heirarchy_directory)

        except FileExistsError:
            print("[WARNING] Directory already exists.")

    def clean_up_files(self):
        for dir_path, dir_names, file_names in os.walk(self.input_directory):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))


if __name__ == "__main__":
    purge_audit_object = PurgeAuditScript(DIRECTORY)
    purge_audit_object.begin_automation()
