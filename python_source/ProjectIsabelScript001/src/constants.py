#!usr/bin/env python
import os


class Constants:
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
    OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
    INPUT_DIR = os.path.join(PROJ_ROOT, "input")
    TEST_DIR = os.path.join(PROJ_ROOT, 'test')

    DATE_FORMAT = '%d-%B-%Y'
    TIME_24_FORMAT = '%H:%M:%S'
    TIF_EXT = '.tif'

    MONTH_NAME = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
