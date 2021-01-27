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
    IMAGES_DIR = os.path.join(ROOT_DIR, 'images')
    TEMPL_DIR = os.path.join(ROOT_DIR, 'templates')

    ROUND_PRECISION = 4
    CSV_FILE_EXT = '.csv'
    EXCEL_FILE_EXT = '.xlsx'
    DOCX_FILE_EXT = '.docx'
    TXT_FILE_EXT = '.txt'
    LDIF_FILE_EXT = '.ldif'

    ATTRIBUTE_KEY = " attributes"
