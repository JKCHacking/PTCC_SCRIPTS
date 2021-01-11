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

    SAFEHEIGHT = "10"
    SKIMHEIGHT = "3"
    STARTHEIGHT = "1"
    CUTDEPTH = "-0.15"
    FEEDRATE = "200"
    DRILLDEPTH = "-1.8"
    DRILLRATE = "30"
    FINISHPOS = "G0 X-100"
    R = 2  # Round off to decimal places
    CIRCLERAD = 0.51  # Maximum circle radius to drill
