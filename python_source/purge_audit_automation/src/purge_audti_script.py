#!usr/bin/env python

from comtypes import client
from comtypes import COMError
from shutil import copyfile
import os

BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
DRAWING_EXTENSION = ".dwg"
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

        self.directory = directory

    def __open_file(self, drawing_full_path):
        print("Opening File: {}".format(drawing_full_path))
        document = None
        if os.path.exists(drawing_full_path):
            self.bricscad_application.Documents.Open(drawing_full_path)
            document = self.bricscad_application.ActiveDocument
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

    def __copy_file_with_extension(self, drawing_full_path, file_name):
        # create a directory where to put all the good stuffs
        file_folder_fullpath = os.path.dirname(drawing_full_path)
        folder_dump = file_folder_fullpath + "_DONE"
        try:
            os.mkdir(folder_dump)
        except FileExistsError:
            print("Directory {} already exists".format(folder_dump))

        new_file_to_dump = os.path.join(folder_dump, file_name)

        try:
            copyfile(drawing_full_path, new_file_to_dump)
        except FileExistsError:
            print("File {} already exists in {}", file_name, folder_dump)

    def __traverse_in_directory(self):
        for dir_path, dir_names, file_names in os.walk(self.directory):
            if "_DONE" not in dir_path:
                for file_name in file_names:
                    file_full_path = os.path.join(dir_path, file_name)
                    if file_full_path.endswith(DRAWING_EXTENSION):
                        self.make_changes_to_drawing(file_full_path)

    def make_changes_to_drawing(self, drawing_full_path):
        file_name = os.path.basename(drawing_full_path)
        document = self.__open_file(drawing_full_path)
        self.__purge_document(document, file_name)
        self.__audit_document(document, file_name)
        self.__save_document(document, file_name)
        self.__copy_file_with_extension(drawing_full_path, file_name)

    def begin_automation(self):
        self.__traverse_in_directory()


if __name__ == "__main__":
    purge_audit_object = PurgeAuditScript(DIRECTORY)
    purge_audit_object.begin_automation()
