#!usr/bin/env python
import os


class Constants:
    BRICS_APP_NAME = "BricscadApp.AcadApplication"  # switch to other app CAD here.

    UTIL_DIR = os.path.dirname(os.path.realpath(__file__))
    SRC_DIR = os.path.dirname(UTIL_DIR)
    ROOT_DIR = os.path.dirname(SRC_DIR)
    TEST_DIR = os.path.join(ROOT_DIR, "test")
    INPUT_DIR = os.path.join(ROOT_DIR, 'input')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')

    JPG_FILE_EXT = '.jpg'
    BMP_FILE_EXT = '.bmp'
    PNG_FILE_EXT = '.png'
    MC_FILE_EXT = '.xmcd'
    DWG_FILE_EXT = '.dwg'
    DXF_FILE_EXT = '.dxf'
    BAK_FILE_EXT = '.bak'
    TXT_FILE_EXT = '.txt'
