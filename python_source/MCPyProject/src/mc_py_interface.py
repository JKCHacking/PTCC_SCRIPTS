#!/usr/bin/env python
import os
import io
import ctypes
import win32clipboard
import time
from src.constants import Constants
from src.logger import Logger
from comtypes import client
from comtypes import COMError
from comtypes.client import Constants as ct_constants
from pywinauto import Application
from pywinauto.keyboard import send_keys
from PIL import Image

logger = Logger()


class MCPyScript:
    def __init__(self, worksheet_fullpath):
        self.logger = logger.get_logger()
        try:
            self.mathcad = client.GetActiveObject(Constants.APP_NAME, dynamic=True)
            self.mathcad.Visible = True
        except (OSError, COMError):
            self.logger.info(f"{Constants.APP_NAME} is not Running...")
            self.logger.info(f"Opening {Constants.APP_NAME}...")
            self.mathcad = client.CreateObject(Constants.APP_NAME, dynamic=True)
            self.mathcad.Visible = True

        self.worksheet_fullpath = worksheet_fullpath
        self.mc_constants = ct_constants(self.mathcad)
        self.user32 = ctypes.windll.user32
        ws_collection = self.mathcad.Worksheets
        self.ws = ws_collection.Open(worksheet_fullpath)

    def get_mchandle(self, ws_filename):
        window_title = f'Mathcad - [{ws_filename}]'
        handle = self.user32.FindWindowW(None, window_title)
        if handle == 0:
            window_title = f'Mathcad - [{ws_filename}.xmcd]'
            handle = self.user32.FindWindowW(None, window_title)
        return handle

    def show_window(self):
        ws_filename = os.path.basename(self.worksheet_fullpath)
        ws_filename = ws_filename.split(".")[0]
        handle = self.get_mchandle(ws_filename)
        mc_app_auto = Application().connect(handle=handle)
        dlg = mc_app_auto.top_window()
        dlg.set_focus()
        time.sleep(2)

    def import_images(self, image_fp_ls):
        offset_next_img = 26

        directory_object_list = []
        for image_fullpath in image_fp_ls:
            image_path_list = []
            img = Image.open(image_fullpath)
            image_name = os.path.basename(image_fullpath).split(".")[0]

            with io.BytesIO() as output:
                img.thumbnail(Constants.IMAGE_SIZE, Image.ANTIALIAS)
                img.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            directory_object_list.append(image_name)
            image_path_list.append(image_name)

            basename = ""
            dirname = image_fullpath
            while basename != "input":
                if basename != "" and basename not in directory_object_list:
                    directory_object_list.append(basename)
                    image_path_list.append(basename)
                dirname = os.path.dirname(dirname)
                basename = os.path.basename(dirname)

            str_command = ""
            for filename in reversed(image_path_list):
                str_command += f"{filename} {Constants.ENTER_KEY} "
            str_command += f"{Constants.PASTE_KEY} {Constants.DOWN_ARROW * offset_next_img}"
            send_keys(str_command)

        if self.ws.NeedsSave:
            self.logger.info("Worksheet has been saved")
            self.ws.Save()
        else:
            self.logger.info("Worksheet does not need to save")
        self.ws.Close()
