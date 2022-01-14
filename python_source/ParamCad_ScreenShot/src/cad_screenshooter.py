import mss
import mss.tools
import os
from ctypes import windll, Structure, c_ulong, byref
from comtypes import client
from comtypes import COMError


SRC_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.dirname(SRC_PATH)
OUTPUT_PATH = os.path.join(APP_PATH, "output")


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
    path = "H:/Desktop/projects/parametric blocks programming/DEMO/U443-A36.dwg"
    bs_app = get_cad_application()
    doc = bs_app.Documents.Open(path)

    input("Choose the upper left point: ")
    ul_point = query_mouse_position()
    print(ul_point)
    input("Choose the lower right point: ")
    lr_point = query_mouse_position()
    print(lr_point)

    param_names = ["MW", "MH"]
    for r in zip(range(100, 200), range(150, 250)):
        param_val = []
        for i, v in enumerate(r):
            edit_parameters(doc, param_names[i], v)
            param_val.append("{}_{}".format(param_names[i], v))
        image_path = os.path.join(OUTPUT_PATH, "_".join(param_val) + ".png")
        screenshot_partial(image_path, ul_point, lr_point)


if __name__ == "__main__":
    main()
