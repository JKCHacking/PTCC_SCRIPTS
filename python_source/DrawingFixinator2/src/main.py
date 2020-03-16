#!usr/bin/env python
from logger import Logger
from constants import Constants
from shutil import copyfile, SameFileError
from comtypes import client
from comtypes import COMError
from purge_audit import PurgeAudit
from fix_layout_name import FixLayoutNameScript
from distutils.dir_util import copy_tree
import os

APP_NAME = Constants.BRICSCAD_APP_NAME   # switch to other app CAD here.
logger = Logger()


class Main:
    def __init__(self):
        self.logger = logger.get_logger()
        try:
            self.cad_application = client.GetActiveObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        except(OSError, COMError):
            self.logger.info(f"{APP_NAME} is not Running...")
            self.logger.info(f"Opening {APP_NAME}...")
            self.cad_application = client.CreateObject(APP_NAME, dynamic=True)
            self.cad_application.Visible = True
        self.script_objects = []
        self.setup()

    @staticmethod
    def setup():
        os.makedirs(Constants.OUTPUT_DIRECTORY, exist_ok=True)
        os.makedirs(Constants.ERROR_DIRECTORY, exist_ok=True)

    @staticmethod
    def _put_in_dict(layouts):
        layout_dict = {}

        for layout in layouts:
            key = layout.TabOrder
            layout_dict[key] = layout

        return layout_dict

    def copy_error_file(self, file_path):
        src = file_path
        dest = os.path.join(Constants.ERROR_DIRECTORY, os.path.basename(file_path))

        try:
            copyfile(src, dest)
            os.remove(file_path)
        except FileExistsError as e:
            self.logger.warn(e)
        except SameFileError as e:
            self.logger.warn(e)

    def start(self, script_objects):
        self.script_objects = script_objects
        self.copy_input_to_output()
        error_files, total_files = self.traverse_in_directory(script_objects)
        self.clean_up_files()
        self.create_summary_log(error_files, total_files)
        self.cad_application.Visible = False

    def clean_up_files(self):
        self.logger.info("Cleaning up files...")
        for dir_path, dir_names, file_names in os.walk(Constants.OUTPUT_DIRECTORY):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.BAK_FILES):
                    os.remove(os.path.join(dir_path, file_name))
        self.logger.info("Cleaning up files done..")

    def copy_input_to_output(self):
        self.logger.info("Copying files...")
        try:
            copy_tree(Constants.INPUT_DIRECTORY, Constants.OUTPUT_DIRECTORY)
        except FileExistsError as e:
            self.logger.warn(e)

    def traverse_in_directory(self, script_objects):
        directory = Constants.OUTPUT_DIRECTORY
        error_files = []
        total_files = 0
        if len(os.listdir(directory)) == 0:
            self.logger.warning(f"The {os.path.basename(directory)} Folder is empty...")
        else:
            for dir_path, dir_names, file_names in os.walk(directory):
                for file_name in file_names:
                    file_full_path = os.path.join(dir_path, file_name)
                    if file_full_path.endswith(Constants.DRAWING_EXTENSION) \
                            and dir_path != Constants.ERROR_DIRECTORY:
                        document = self.open_file(file_full_path)
                        total_files = total_files + 1
                        if document:
                            for script_object in script_objects:
                                script_object.begin_automation(document, file_name)
                            self.save_document(document, file_name)
                        else:
                            self.copy_error_file(file_full_path)
                            error_files.append(file_full_path)
        return error_files, total_files

    def open_file(self, drawing_full_path):
        self.logger.info("Opening File: {}".format(drawing_full_path))
        document = None
        if os.path.exists(drawing_full_path):
            try:
                self.cad_application.Documents.Open(drawing_full_path)
                document = self.cad_application.ActiveDocument
            except COMError:
                self.logger.error("[ERROR]Invalid Drawing File!: {}".format(drawing_full_path))
        return document

    def save_document(self, document, file_name):
        self.logger.info("Saving changes to Drawing: {}".format(file_name))
        if not document.Saved:
            self.logger.info("There are unsaved changes in the Drawing")
            self.__zoom_extends_first_layout(document)
            document.Save()
            self.cad_application.Documents.Close()
        self.logger.info("Saving done and Closed...")

    def __zoom_extends_first_layout(self, document):
        layouts = document.Layouts
        layout_dict = self._put_in_dict(layouts)
        for tab_order, layout in sorted(layout_dict.items()):
            document.ActiveLayout = layout
            self.cad_application.ZoomExtents()
            document.SetVariable("TREEDEPTH", document.GetVariable("TREEDEPTH"))
            # command_str = "._ZOOM\nextents\n"
            # document.SendCommand(command_str)

        document.ActiveLayout = layout_dict[1]

    def create_summary_log(self, error_files, total_files):
        log_file_path = os.path.join(Constants.OUTPUT_DIRECTORY, "log.txt")
        log_file = open(log_file_path, "w")
        total_errors_found = len(error_files)
        script_names = [str(type(script)) for script in self.script_objects]

        log_file.write("=============SUMMARY===============\n")
        log_file.write(f"Total Number of Drawings: {total_files}\n")
        log_file.write(f"Total Drawings with Errors: {total_errors_found}\n")
        log_file.write(f"Scripts used: {script_names}")
        log_file.close()


if __name__ == "__main__":
    print("1. Purge and Audit = pa")
    print("2. Fix Layout Names = fln")
    correct_commands = ["pa", "fln"]
    script_name = input("Select scripts to apply to the drawings: ")
    script_name_list = script_name.split(",")

    script_object_list = []

    for input_script_command in script_name_list:
        if input_script_command in correct_commands:
            if input_script_command == "pa":
                purge_audit = PurgeAudit()
                script_object_list.append(purge_audit)
            if input_script_command == "fln":
                fix_layout_name = FixLayoutNameScript()
                script_object_list.append(fix_layout_name)
        else:
            print("Something is wrong with your input, please check again...")
            script_object_list.clear()
            break

    if script_object_list:
        main_script = Main()
        main_script.start(script_object_list)
