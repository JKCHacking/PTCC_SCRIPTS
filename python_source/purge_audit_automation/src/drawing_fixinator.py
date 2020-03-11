#!/usr/bin/env python

#################################
# Author: Joshnee Kim B. Cunanan
# last Modified: 09 March 2020
# Version: 1.0
#################################

import os
from shutil import copytree
from tkinter import messagebox
from tkinter import Tk
from logger import Logger
import array
from purge_audit_script import PurgeAuditScript

SELECT_ALL = 5
SELECTION_SET_NAME = "PROJECTXX_SS"
BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
AUTOCAD_APP_NAME = "AutoCAD.Application"
APP_NAME = AUTOCAD_APP_NAME  # switch to other app CAD here.
DRAWING_EXTENSION = ".dwg"

SRC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIRECTORY = os.path.join(os.path.dirname(SRC_DIRECTORY), "output")
ERROR_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "error")
FIX_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "fix")

acAttachmentPointBottomCenter = 1
acAttachmentPointBottomLeft = 2
acAttachmentPointBottomRight = 3
acAttachmentPointMiddleCenter = 4
acAttachmentPointMiddleLeft = 5
acAttachmentPointMiddleRight = 6
acAttachmentPointTopCenter = 7
acAttachmentPointTopLeft = 8
acAttachmentPointTopRight = 9

logger = Logger()


class DrawingFixinator(PurgeAuditScript):
    def __init__(self):
        root = Tk()
        root.withdraw()
        self.logger = logger.get_logger()
        super().__init__(SRC_DIRECTORY)
        os.makedirs(FIX_DIRECTORY, exist_ok=True)

    def begin_automation(self):
        self.scan_for_issue()

    def create_prompt(self):
        response = messagebox.askquestion("Fix Issues", "There are errors detected, Do you want to fix it?",
                                          icon="warning")
        if response == 'yes':
            # self.__fix_wrong_tab_name()
            self.__realign_text()
        elif response == 'no':
            self.cad_application.Visible = False

    def scan_for_issue(self):
        self.logger.info("Scanning for issues...")
        # This only supports checking of wrong tab names for now.
        wrong_tab_name_dir_err = os.path.join(ERROR_DIRECTORY, "wrong_tab_name")

        if os.path.exists(ERROR_DIRECTORY):
            if os.path.exists(wrong_tab_name_dir_err) and \
                    len(os.listdir(wrong_tab_name_dir_err)) > 0:
                self.create_prompt()
        else:
            messagebox.showinfo("Fix Issues", "No Errors Found!")
            self.cad_application.Visible = False

    def __fix_cant_open(self):
        pass

    def __realign_text(self):
        self.logger.info("Re aligning Text...")
        wrong_tab_name_dir_err = os.path.join(ERROR_DIRECTORY, "wrong_tab_name")
        realigned_dir_fix = os.path.join(FIX_DIRECTORY, "re_aligned")

        try:
            copytree(wrong_tab_name_dir_err, realigned_dir_fix)
        except FileExistsError as e:
            self.logger.warning(e)

        for dir_path, dir_names, file_names in os.walk(realigned_dir_fix):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(DRAWING_EXTENSION):
                    document = self._open_file(file_full_path)
                    if document:
                        for ps_object in document.PaperSpace:
                            if ps_object.ObjectName == "AcDbMLeader":
                                vertices_coordinate = ps_object.GetLeaderLineVertices(0)
                                pt1 = array.array('d', [0.0, 0.0, 0.0])
                                pt2 = array.array('d', [vertices_coordinate[0], vertices_coordinate[1], vertices_coordinate[2]])
                                ps_object.Move(pt2, pt1)
                                ps_object.Move(pt1, pt2)

                        self._save_document(document, file_name)
        self.clean_up_files(realigned_dir_fix)
        # self.cad_application.Visible = False

    @staticmethod
    def __get_selection_set(document, filter_types, filter_data):
        try:
            selection_sets = document.SelectionSets.Add(SELECTION_SET_NAME)
        except:  # TODO: Create custom error class for pylint warnings
            selection_sets = document.SelectionSets.Item(SELECTION_SET_NAME)

        pt1 = array.array('d', [0.0, 0.0, 0.0])
        pt2 = array.array('d', [0.0, 0.0, 0.0])

        selection_sets.Select(SELECT_ALL, pt1, pt2, filter_types, filter_data)

        return selection_sets

    def __fix_wrong_tab_name(self):
        self.logger.info("Fixing wrong tab names...")
        wrong_tab_name_dir_err = os.path.join(ERROR_DIRECTORY, "wrong_tab_name")
        wrong_tab_name_dir_fix = os.path.join(FIX_DIRECTORY, "wrong_tab_name")

        try:
            copytree(wrong_tab_name_dir_err, wrong_tab_name_dir_fix)
        except FileExistsError as e:
            self.logger.warning(e)

        for dir_path, dir_names, file_names in os.walk(wrong_tab_name_dir_fix):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(DRAWING_EXTENSION):
                    document = self._open_file(file_full_path)
                    self._apply_standards(document, file_name, fix=True)
                    self._save_document(document, file_name)

        self.clean_up_files(wrong_tab_name_dir_fix)
        messagebox.showinfo("Fix Issues", "Fixing done!")
        self.cad_application.Visible = False


if __name__ == "__main__":
    drawing_fixinator = DrawingFixinator()
    drawing_fixinator.begin_automation()
