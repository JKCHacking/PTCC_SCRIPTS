#!usr/bin/env python
import os


class Constants:
    APP_NAME = "Mathcad.Application"  # switch to other app CAD here.

    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
    OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
    INPUT_DIR = os.path.join(PROJ_ROOT, "input")
    TEST_DIR = os.path.join(PROJ_ROOT, 'test')

    JPG_FILE_EXT = '.jpg'
    MC_FILE_EXT = '.xmcd'

    IMAGE_SIZE = 250, 250
