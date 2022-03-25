import tkinter
import os
from comtypes import client
from comtypes import COMError
from tkinter.filedialog import askopenfilename


def get_solids(doc):
    solids = []
    model_space = doc.ModelSpace
    for obj in model_space:
        if obj.ObjectName == "AcDb3dSolid" and obj.Visible:
            solids.append(obj)
    return solids


def get_cad_application():
    b_cad_guid = "BricscadApp.AcadApplication"
    try:
        b_cad_app = client.GetActiveObject(b_cad_guid, dynamic=True)
    except COMError:
        b_cad_app = client.CreateObject(b_cad_guid, dynamic=True)
    b_cad_app.Visible = True
    return b_cad_app


def get_color_cat(objects):
    ac_color_method_by_aci = 195
    color_categories = []
    for obj in objects:
        if obj.TrueColor.ColorMethod == ac_color_method_by_aci:
            color_index = obj.TrueColor.ColorIndex
            if color_index not in color_categories:
                color_categories.append(color_index)
    return color_categories


def delete_except_cat(doc, category):
    doc.SendCommand(
        '(setq ss (ssget "_X" \'((0 . "3DSOLID")(-4 . "<>")(62 . {category}))))\n(if ss (command "_.Erase" ss ""))\n'
        .format(category=category))


def main():
    tkinter.Tk().withdraw()
    dwg_path = askopenfilename(title="Select the main DWG", filetypes=[("DWG Files", ".dwg")])
    cad = get_cad_application()
    doc = cad.Documents.Open(dwg_path)
    solids = get_solids(doc)
    color_categories = get_color_cat(solids)
    for color_category in color_categories:
        print("Saving solids from color index: {}".format(color_category))
        delete_except_cat(doc, color_category)
        doc.SaveAs(os.path.join(doc.Path, "{cat}.dwg".format(cat=color_category)))
        doc.Close()
        doc = cad.Documents.Open(dwg_path)


if __name__ == "__main__":
    main()
