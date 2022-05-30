#!usr/bin/env python
import os


class Constants:
    BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
    AUTOCAD_APP_NAME = "AutoCAD.Application"
    APP_NAME = BRICSCAD_APP_NAME  # switch to other app CAD here.

    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
    OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
    INPUT_DIR = os.path.join(PROJ_ROOT, "input")

    BAK_FILES = ".bak"
