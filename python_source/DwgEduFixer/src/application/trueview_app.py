import os
import ctypes
import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
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
        # self.tv_app.top_window().wait('ready')
        time.sleep(5)

    def show_window(self):
        dlg = self.tv_app.top_window()
        dlg.set_focus()

    def open_file(self, file_full_path):
        if os.path.exists(file_full_path):
            self.show_window()

            # show the select file window
            str_command = f"%fo"
            send_keys(str_command)
            # wait for the file window to appear
            self.wait_window_by_title('Select File')
            # type the file name
            str_command = f'+{{VK_END}}{{DELETE}}{file_full_path}~'
            send_keys(str_command, with_spaces=True)
        else:
            self.logger.error("File not found: {file_full_path}")

    def wait_window_by_title(self, title):
        found = True
        try:
            self.tv_app.window(title_re=title).wait('visible', timeout=5, retry_interval=0.5)
        except TimeoutError:
            self.logger.warning(f"Waiting time expired, Window with title {title} was not found.")
            found = False
        return found

    def get_handle_by_title(self, title):
        handle = 0
        if self.wait_window_by_title(title):
            handle = self.user32.FindWindowW(None, title)
        return handle

    def close_top_window(self):
        send_keys("%{F4}")

    def exit_app(self):
        self.logger.info(f"Exiting DWG TrueViewer...")
        self.tv_app.kill()
