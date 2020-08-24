import os
import pywinauto
import win32clipboard
from dateutil.parser import parse
from pywinauto.keyboard import send_keys
from src.util.logger import get_logger

util_logger = get_logger("UtilLogger")


class Utilities:
    @staticmethod
    def copy_to_cb(text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

    @staticmethod
    def send_command(command):
        send_keys(command)

    @staticmethod
    def get_handle_by_title(title):
        handle = pywinauto.findwindows.find_windows(title_re=title)
        return handle

    @staticmethod
    def activate_window(handle):
        app = pywinauto.application.Application().connect(handle=handle)
        window = app.top_window()
        window.set_focus()

    @staticmethod
    def clean_up_file(ext_list, directory):
        util_logger.info("Removing unnecessary files...")
        for dir_path, dir_names, file_names in os.walk(directory):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                ext = os.path.splitext(file_full_path)[1]
                if ext in ext_list:
                    os.remove(file_full_path)

    @staticmethod
    def is_date(date_str, fuzzy=False):
        try:
            parse(date_str, fuzzy=fuzzy)
            date_bool = True
        except ValueError:
            date_bool = False
        return date_bool
