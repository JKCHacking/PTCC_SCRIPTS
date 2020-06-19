#!/usr/bin/env python
from src.mc_py_interface import MCPyScript
from src.file_manager import FileManager
import time

if __name__ == "__main__":
    fm = FileManager()
    template_ws_path = fm.get_template_ws()
    image_fp_ls = fm.get_image_list()

    mc_py_script = MCPyScript(template_ws_path)
    mc_py_script.show_window()
    # make sure that the window is already showing.
    time.sleep(1)
    mc_py_script.import_images(image_fp_ls)
