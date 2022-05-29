#!usr/bin/env python

from logger import Logger
from drawing_script import DrawingScript
from constants import Constants
import os


class LayoutNameScanner(DrawingScript):
    def __init__(self):
        self.logger = Logger().get_logger()

    def begin_automation(self, document, file_name):
        self.logger.info(f"Starting scipt: LayoutNameScanner")
        self.__scan_layout_name(document, file_name)

    def __scan_layout_name(self, document, file_name):
        self.logger.info("Fixing Layout Names....")
        self._traverse_layout_document(document, file_name)

    def _traverse_layout_document(self, document, file_name):
        self.logger.info(f"Traversing {file_name} document layouts...")
        file_name = file_name.split(".")[0]
        file_name_list = file_name.split("-")
        document_counter = file_name_list[len(file_name_list) - 1]  # gets the last element in the list.
        counter_digit_num = len(document_counter)
        post_fix_count = "0000"

        if document_counter.isdigit():
            post_fix_count = file_name_list.pop()

        post_fix_count_int = int(post_fix_count)
        layouts = document.Layouts
        layout_dict = self._put_in_dict(layouts)

        for tab_order, layout in sorted(layout_dict.items()):
            current_layout_name = layout.Name
            document.ActiveLayout = layout
            post_fix_count_str = str(post_fix_count_int).zfill(counter_digit_num)
            post_fix_count_str = "" if int(post_fix_count_str) == 0 else post_fix_count_str
            prefix_file_name = "-".join(file_name_list)
            expected_layout_name = "-".join([prefix_file_name, post_fix_count_str])

            if current_layout_name != "Model":
                if current_layout_name != expected_layout_name:
                    self.__save_as(document, file_name)
                    break
                post_fix_count_int = post_fix_count_int + 1

    @staticmethod
    def __save_as(document, file_name):
        document_full_path = os.path.join(Constants.WRONG_TEMPLATE_NAME, file_name)
        document.SaveAs(document_full_path)

    @staticmethod
    def _put_in_dict(layouts):
        layout_dict = {}

        for layout in layouts:
            key = layout.TabOrder
            layout_dict[key] = layout

        return layout_dict
