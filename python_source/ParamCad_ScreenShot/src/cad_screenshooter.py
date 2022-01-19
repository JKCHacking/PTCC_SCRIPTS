import mss
import mss.tools
import os
import tkinter
import numpy
import json
from PIL import Image
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


def make_image_hd(image_path):
    image_file = Image.open(image_path)
    image_file = image_file.resize((1920, 1080), Image.ANTIALIAS)
    image_file.save(image_path, quality=95)


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
    changes_json_file = askopenfilename(title="Select the Changes JSON file", filetypes=[("JSON Files", ".json")])
    with open(changes_json_file, 'r') as json_file:
        changes = json.load(json_file)

    for change in changes:
        doc.StartUndoMark()
        for i in numpy.linspace(change["start"], change["stop"] + 1, num_frames):
            step = round(i, 3)
            print("Creating screenshot for {} = {}".format(change["param_name"], step))
            doc.ActiveSpace = ACMODELSPACE
            edit_parameters(doc, change["param_name"], step)
            doc.ActiveSpace = ACPAPERSPACE
            image_path = os.path.join(OUTPUT_PATH, "{}_{}.png".format(change["param_name"], step))
            screenshot_partial(image_path, ul_point, lr_point)
            make_image_hd(image_path)
        doc.EndUndoMark()
        doc.SendCommand("_U\n")
        doc.SendCommand("REGEN\n")


if __name__ == "__main__":
    main()
