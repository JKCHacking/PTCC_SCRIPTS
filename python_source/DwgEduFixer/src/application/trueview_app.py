import os
import ctypes
import time
import win32clipboard
from pywinauto.application import Application
from pywinauto.timings import TimeoutError
from src.util.logger import get_logger


class TrueViewerApp:
    def __init__(self):
        self.logger = get_logger("TrueViewerAppLogger")
        self.user32 = ctypes.windll.user32
        self.tv_app = None

    def start_app(self):
        self.logger.info(f"Starting DWG TrueViewer...")
        # open trueview by executing the dwgviewr.exe
        tv_exec = "C:\\Program Files\\Autodesk\\DWG TrueView 2020 - English\\dwgviewr.exe"
        self.tv_app = Application(backend='win32').start(tv_exec)
        time.sleep(5)

    def open_file(self, file_full_path):
        dialog_list = []
        select_file_command = "^o"
        clear_text_command = '+{VK_END}{DELETE}'
        paste_command = '^v'
        enter_command = '~'
        close_tab_command = "^{F4}"

        if os.path.exists(file_full_path):
            # copy file_full_path to clipboard
            self.__copy_text_to_cb(file_full_path)
            file_window = False
            # we should wait for the Select File Window to open,
            # if the file should be opened.
            while not file_window:
                self.__send_command(select_file_command)
                # wait for the file window to appear
                file_window = self.wait_window_by_title('Select File', 2)
            # clear text then paste to select file window
            self.__send_command(clear_text_command + paste_command + enter_command, with_spaces=True)
            # check if a dialog is displayed
            self.__close_n_save_dialog(dialog_list, 2)
            if self.tv_app.top_window().texts()[0] == '':  # opened drawings tabs are not dialog windows
                self.__close_n_save_dialog(dialog_list, 2)
                # close the drawing tab
                self.__send_command(close_tab_command)
        else:
            self.logger.error("File not found: {file_full_path}")
        return dialog_list

    def wait_window_by_title(self, title, timeout):
        found = True
        try:
            self.tv_app.window(title_re=title).wait('ready', timeout=timeout, retry_interval=0.5)
        except TimeoutError:
            self.logger.warning(f'Waiting time expired, Window with title "{title}" was not found.')
            found = False
        return found

    def get_handle_by_title(self, title):
        handle = 0
        if self.wait_window_by_title(title, 2):
            handle = self.user32.FindWindowW(None, title)
        return handle

    def exit_app(self):
        self.logger.info(f"Exiting DWG TrueViewer...")
        self.tv_app.kill()

    def __close_n_save_dialog(self, dialog_list, sec):
        time.sleep(sec)  # sometimes the application takes time to initiate the open of the file.
        close_window_command = "%{F4}"
        top_window_title = self.tv_app.top_window().texts()[0]
        if 'Student' in top_window_title:  # a dialog is displayed as the top window
            dialog_list.append(top_window_title)
            self.__send_command(close_window_command)
        elif 'Foreign' in top_window_title:
            dialog_list.append(top_window_title)
            self.__send_command(close_window_command)
        elif 'References - Not Found Files' in top_window_title:
            dialog_list.append(top_window_title)
            self.__send_command(close_window_command)

    def __send_command(self, command, with_spaces=False):
        self.tv_app.top_window().type_keys(command, with_spaces=with_spaces)

    @staticmethod
    def __copy_text_to_cb(text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
