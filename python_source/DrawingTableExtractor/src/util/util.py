import pywinauto
import win32clipboard
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

