#!/usr/bin/env python
from src.mc_py_interface import MCPyScript
from src.constants import Constants
import os

if __name__ == "__main__":
    mc_file_path = os.path.join(Constants.INPUT_DIR, "test.xmcd")

    mc_py_script = MCPyScript()
    mc_py_script.evaluate_mathcad(mc_file_path)