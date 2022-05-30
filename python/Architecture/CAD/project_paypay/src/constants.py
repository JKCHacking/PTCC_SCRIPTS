#!usr/bin/env python
import os


class Constants:
    MAX_OPENING = 354.0
    TOP_TO_PIVOTAL = 92.0
    FIR_BRACK_DIST = 169.6

    R_BRACK_ORIG_ANG = 90.0
    R_BRACK_ORIG_LEN = 50.0
    L_BRACK_ORIG_ANG = 90.0
    L_BRACK_ORIG_LEN = 50.0

    BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
    AUTOCAD_APP_NAME = "AutoCAD.Application"
    APP_NAME = BRICSCAD_APP_NAME  # switch to other app CAD here.
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
    OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
    INPUT_DIR = os.path.join(PROJ_ROOT, "input")

    BAK_FILES = ".bak"

    UPPER_EDGE = 1
    LOWER_EDGE = 4
    RIGHT_EDGE = 2
    LEFT_EDGE = 8
    UPPER_RIGHT_LOWER_EDGE = 7