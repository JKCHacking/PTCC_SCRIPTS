import os


class Constants:
    UTIL_DIR = os.path.dirname(os.path.realpath(__file__))
    SRC_DIR = os.path.dirname(UTIL_DIR)
    ROOT_DIR = os.path.dirname(SRC_DIR)
    TEST_DIR = os.path.join(ROOT_DIR, "test")
    INPUT_DIR = os.path.join(os.path.dirname(ROOT_DIR), "input")
    OUTPUT_DIR = os.path.join(os.path.dirname(ROOT_DIR), "output")
    FILES_DIR = os.path.join(ROOT_DIR, "files")

    EXCEL_EXT = ".xlsx"
