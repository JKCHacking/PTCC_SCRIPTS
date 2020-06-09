#!usr/bin/env python
import os


class Constants:
    APP_NAME = "Mathcad.Application"  # switch to other app CAD here.

    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_ROOT = os.path.dirname(SCRIPT_DIR)
    OUTPUT_DIR = os.path.join(PROJ_ROOT, "output")
    INPUT_DIR = os.path.join(PROJ_ROOT, "input")
    TEST_DIR = os.path.join(PROJ_ROOT, 'test')

    BAK_FILES = ".bak"

    TIME_12_FORMAT = '%I:%M %p'
    TIME_24_FORMAT = '%H:%M:%S'

    DATE_FORMAT = '%d-%B-%Y'
    DAY_LIST = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    HOLIDAY_LIST = ['January 01, 2020',
                    'January 25, 2020',
                    'February 25, 2020',
                    'April 09, 2020',
                    'April 10, 2020',
                    'April 11, 2020',
                    'May 01, 2020',
                    'May 23, 2020',
                    'June 12, 2020',
                    'July 31, 2020',
                    'August 21, 2020',
                    'August 31, 2020',
                    'November 01, 2020',
                    'November 02, 2020',
                    'November 30, 2020',
                    'December 24, 2020',
                    'December 25, 2020',
                    'December 30, 2020',
                    'December 31, 2020']

