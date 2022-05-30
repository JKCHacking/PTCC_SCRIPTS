import os


class Constants:
    SRC_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR = os.path.dirname(SRC_DIR)
    PROJ_DIR = os.path.dirname(APP_DIR)
    INPUT_DIR = os.path.join(PROJ_DIR, "input")
    OUTPUT_DIR = os.path.join(PROJ_DIR, "output")
