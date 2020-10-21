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

    JPG_FILE_EXT = '.jpg'
    BMP_FILE_EXT = '.bmp'
    PNG_FILE_EXT = '.png'
    MC_FILE_EXT = '.xmcd'
    DWG_FILE_EXT = '.dwg'
    DXF_FILE_EXT = '.dxf'
    BAK_FILE_EXT = '.bak'
    TXT_FILE_EXT = '.txt'

    ROUND_PRECISION = 5

    IMAGE_WIDTH = 200
    IMAGE_HEIGHT = 50

    FIGURE_WIDTH = 12
    FIGURE_HEIGHT = 15

    INS_UNITS = {
        0: "Unitless",
        1: "Inches",
        2: "Feet",
        3: "Miles",
        4: "Millimeters",
        5: "Centimeters",
        6: "Meters",
        7: "Kilometers",
        8: "Microinches",
        9: "Mils",
        10: "Yards",
        11: "Angstroms",
        12: "Nanometers",
        13: "Microns",
        14: "Decimeters",
        15: "Decameters",
        16: "Hectometers",
        17: "Gigameters",
        18: "Astronomical Units",
        19: "Light Years",
        20: "Parsecs",
        21: "US Survey Feet",
        22: "US Survey Inch",
        23: "US Survey Yard",
        24: "US Survey Mile"
    }
