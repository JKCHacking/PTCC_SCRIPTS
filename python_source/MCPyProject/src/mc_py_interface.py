#!/usr/bin/env python
import os
import io
import ctypes
import win32clipboard
from src.constants import Constants
from src.logger import Logger
from src.file_manager import FileManager
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
        return handle

    def show_window(self):
        ws_filename = os.path.basename(self.worksheet_fullpath)
        ws_filename = ws_filename.split(".")[0]
        handle = self.get_mchandle(ws_filename)
        mc_app_auto = Application().connect(handle=handle)
        dlg = mc_app_auto.top_window()
        dlg.set_focus()

    def import_images(self):
        fm = FileManager()
        image_fp_ls = fm.get_image_list()
        offset_next_img = 26
        offset_name_img = 10
        offset_row_origin = offset_name_img

        for image_fullpath in image_fp_ls:
            img = Image.open(image_fullpath)
            width, height = img.size
            self.logger.info(f'Width: {width} Height: {height}')
            image_name = os.path.basename(image_fullpath).split(".")[0]

            with io.BytesIO() as output:
                img.thumbnail(Constants.IMAGE_SIZE, Image.ANTIALIAS)
                img.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            str_command = f"{Constants.PASTE_KEY}{Constants.DOWN_ARROW * offset_next_img}" + \
                          f"{Constants.RIGHT_ARROW * offset_name_img}{image_name}{Constants.ENTER_KEY}" + \
                          f"{Constants.LEFT_ARROW * offset_row_origin}"
            send_keys(str_command)

        if self.ws.NeedsSave:
            self.logger.info("Worksheet has been saved")
            self.ws.Save()
        else:
            self.logger.info("Worksheet does not need to save")
        # self.ws.Close()
