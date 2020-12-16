import subprocess
import threading
import msgbox as util
import uno


def PdfFileExecutor(*args):
    '''Opens a pdf file linked from the spreadsheet'''
    evt = args[0]
    button_name = evt.Source.Model.Name
    button_label = evt.Source.Model.Label

    # MsgBox("Button Name: {} Button Label: {}".format(button_name, button_label))

    # local_context = uno.getComponentContext()
    # resolver = local_context.ServiceManager.createInstanceWithContext(
    #     "com.sun.star.bridge.UnoUrlResolver", local_context
    # )
    # ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    # smgr = ctx.ServiceManager
    # desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

    # desktop = XSCRIPTCONTEXT.getDesktop()
    # model = desktop.getCurrentComponent()
    #
    # active_sheet = model.CurrentController.ActiveSheet
    # cell1 = active_sheet.getCellRangeByName("A1")
    # cell1.String = str(dir(args))
    # cell2 = active_sheet.getCellRangeByName("A2")
    # cell2.String = str(type(args))

    t1 = threading.Thread(target=pdf_thread_func, args=(button_label,))
    t1.start()


def pdf_thread_func(button_label):
    MsgBox("Button label: {}".format(button_label))
    if button_label == "test.pdf page 10":
        subprocess.run(["C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe",
                        "/A",
                        "page=10",
                        "H:/Desktop/projects/libreoffice_hyperlink/test.pdf"],
                       shell=True)
    elif button_label == "test2.pdf page 5":
        subprocess.run(["C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe",
                        "/A",
                        "page=5",
                        "H:/Desktop/projects/libreoffice_hyperlink/test2.pdf"],
                       shell=True)


def MsgBox(txt):
    mb = util.MsgBox(uno.getComponentContext())
    mb.addButton("OK")
    mb.show(txt, 0, "Python")


if __name__ == "__main__":
    PdfFileExecutor()
