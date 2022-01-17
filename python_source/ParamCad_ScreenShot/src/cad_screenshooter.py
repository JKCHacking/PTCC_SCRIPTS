import mss
import mss.tools
import os
import tkinter
from ctypes import windll, Structure, c_ulong, byref
from comtypes import client
from comtypes import COMError
from tkinter.filedialog import askopenfilename

SRC_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(SRC_PATH)
OUTPUT_PATH = os.path.join(APP_PATH, "output")
ACPAPERSPACE = 0
ACMODELSPACE = 1


def get_cad_application():
    b_cad = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    except COMError:
        b_cad_app = client.CreateObject(b_cad, dynamic=True)
        b_cad_app.Visible = True
    return b_cad_app


def screenshot_partial(filename, ul_point, lr_point):
    with mss.mss() as sct:
        monitor_num = 2
        # screenshot bounding box
        monitor = {
            "top": ul_point["y"],
            "left": ul_point["x"],
            "width": lr_point["x"] - ul_point["x"],
            "height": lr_point["y"] - ul_point["y"],
            "mon": monitor_num
        }
    sct_image = sct.grab(monitor)
    mss.tools.to_png(sct_image.rgb, sct_image.size, output=filename)


def edit_parameters(doc, param_name, value):
    doc.SendCommand("-PARAMETERS edit {} {}\n".format(param_name, value))
    doc.SendCommand("REGEN\n")


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def query_mouse_position():
    pt = POINT()
    user32 = windll.user32
    user32.SetProcessDPIAware()
    user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


def main():
    tkinter.Tk().withdraw()
    path = askopenfilename(title="Select a DWG file", filetypes=[("DWG Files", ".dwg")])
    bs_app = get_cad_application()
    doc = bs_app.Documents.Open(path)

    input("Choose the upper left point: ")
    ul_point = query_mouse_position()
    print(ul_point)
    input("Choose the lower right point: ")
    lr_point = query_mouse_position()
    print(lr_point)

    num_frames = int(input("input number of frames per parameter: "))
    changes = [
        {
            "param_name": "MW",
            "start": 100,
            "stop": 110
        },
        {
            "param_name": "MH",
            "start": 150,
            "stop": 160
        },
        {
            "param_name": "PW",
            "start": 50,
            "stop": 60
        },
        {
            "param_name": "PH",
            "start": 90,
            "stop": 100
        }
    ]

    for change in changes:
        doc.StartUndoMark()
        for i in range(change["start"], change["stop"] + 1, int((change["stop"] - change["start"]) / num_frames)):
            print("Creating screenshot for {} = {}".format(change["param_name"], i))
            doc.ActiveSpace = ACMODELSPACE
            edit_parameters(doc, change["param_name"], i)
            doc.ActiveSpace = ACPAPERSPACE
            image_path = os.path.join(OUTPUT_PATH, "{}_{}.png".format(change["param_name"], i))
            screenshot_partial(image_path, ul_point, lr_point)
        doc.EndUndoMark()
        doc.SendCommand("_U\n")
        doc.SendCommand("REGEN\n")


if __name__ == "__main__":
    main()
