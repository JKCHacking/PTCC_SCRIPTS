import win32clipboard
from pywinauto.keyboard import send_keys


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
