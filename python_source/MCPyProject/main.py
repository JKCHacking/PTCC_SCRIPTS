#!/usr/bin/env python
from src.mc_py_interface import MCPyScript
from src.file_manager import FileManager
import time

if __name__ == "__main__":
    fm = FileManager()
    ws_path_list = fm.get_ws_fp_ls()

    mc_py_script = MCPyScript(ws_path_list[0])
    mc_py_script.show_window()
    # make sure that the window is already showing.
    time.sleep(1)
    mc_py_script.import_images()
