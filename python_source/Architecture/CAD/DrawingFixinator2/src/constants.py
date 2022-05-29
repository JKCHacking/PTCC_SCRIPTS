import os


class Constants:
    SRC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    OUTPUT_DIRECTORY = os.path.join(os.path.dirname(SRC_DIRECTORY), "output")
    INPUT_DIRECTORY = os.path.join(os.path.dirname(SRC_DIRECTORY), "input")
    ERROR_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "error")
    WRONG_TEMPLATE_NAME = os.path.join(OUTPUT_DIRECTORY, "wrong_template_name")
    BRICSCAD_APP_NAME = "BricscadApp.AcadApplication"
    AUTOCAD_APP_NAME = "AutoCAD.Application"
    DRAWING_EXTENSION = ".dwg"
    BAK_FILES = ".bak"
