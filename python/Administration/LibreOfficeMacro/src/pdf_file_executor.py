import os
import subprocess
import threading
import msgbox as util
import uno
from urllib.parse import urlparse


def PdfFileExecutor(*args):
    '''Opens a pdf file linked from the spreadsheet'''
    evt = args[0]
    button_label = evt.Source.Model.Label

    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    uri = model.getURL()
    p = urlparse(uri)
    doc_dir = os.path.dirname(p.path[1:-1])
    # doc_dir = "X:/Office/joshnee/ADMIN_PROJECTS/libreoffice_hyperlink/with_macro"

    active_sheet = model.CurrentController.ActiveSheet
    cell1 = active_sheet.getCellRangeByName("A1")
    cell1.String = str(uri)

    t1 = threading.Thread(target=pdf_thread_func, args=(button_label, doc_dir))
    t1.start()


def pdf_thread_func(button_label, document_dir):
    MsgBox(document_dir)
    file_name, page_num = button_label.split(" ")
    if file_name and page_num:
        subprocess.run(["C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe",
                        "/A",
                        page_num,
                        os.path.join(document_dir, file_name)],
                       shell=True)
    else:
        MsgBox("Invalid Button Name format!")


def MsgBox(txt):
    mb = util.MsgBox(uno.getComponentContext())
    mb.addButton("OK")
    mb.show(txt, 0, "Python")


if __name__ == "__main__":
    PdfFileExecutor()
