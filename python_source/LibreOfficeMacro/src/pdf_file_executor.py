import uno
from pythonscript import ScriptContext
import sys
import subprocess


def PdfFileExecutor(*args):
    '''Opens a pdf file linked from the spreadsheet'''
    subprocess.run(["C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe",
                    "/A",
                    "page=10",
                    "H:/Desktop/projects/libreoffice_hyperlink/test.pdf"],
                   shell=True,
                   check=True)
