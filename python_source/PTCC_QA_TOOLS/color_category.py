import tkinter
import os
from comtypes import client
from comtypes import COMError
from comtypes import automation
from tkinter.filedialog import askopenfilename


def get_solids(doc):
    solids = []
    model_space = doc.ModelSpace
    for obj in model_space:
        if obj.ObjectName == "AcDb3dSolid" and obj.Visible:
            solids.append(obj)
    return solids


def get_solid_by_layer(doc, layer):
    solids = []
    model_space = doc.ModelSpace
    for obj in model_space:
        if obj.ObjectName == "AcDb3dSolid" and obj.Visible and obj.Layer == layer:
            solids.append(obj)
    return solids


def get_solid_by_ci(doc, ic):
    solids = []
    model_space = doc.ModelSpace
    for obj in model_space:
        if obj.ObjectName == "AcDbSolid" and obj.Visible and obj.TrueColor.ColorIndex == ic:
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


def main():
    tkinter.Tk().withdraw()
    dwg_path = askopenfilename(title="Select the main DWG", filetypes=[("DWG Files", ".dwg")])
    cad = get_cad_application()
    doc = cad.Documents.Open(dwg_path)

    try:
        doc.SelectionSets.Item("SELECT GRID").Delete()
    except COMError:
        pass
    selection_set = doc.SelectionSets.Add("SELECT GRID")
    selection_set.SelectOnScreen(automation.VARIANT([0]), automation.VARIANT(["INSERT"]))
    grid_line = selection_set.Item(0)
    solids = get_solids(doc)

    ac_color_method_by_layer = 192
    ac_color_method_by_aci = 195
    ac_color_method_by_rgb = 194
    layer_taken = []
    ci_taken = []
    for solid in solids:
        res_solids = []
        out_file_name = ""
        color_index = solid.TrueColor.ColorIndex
        layer_name = solid.Layer
        if solid.TrueColor.ColorMethod == ac_color_method_by_layer and layer_name not in layer_taken:
            print("Working with layer: {}".format(layer_name))
            res_solids = get_solid_by_layer(doc, layer_name)
            out_file_name = layer_name
            layer_taken.append(layer_name)
        elif (solid.TrueColor.ColorMethod == ac_color_method_by_aci or
              solid.TrueColor.ColorMethod == ac_color_method_by_rgb) and color_index not in ci_taken:
            print("Working with color index: {}".format(color_index))
            res_solids = get_solid_by_ci(doc, color_index)
            out_file_name = color_index
            ci_taken.append(color_index)

        if res_solids:
            if grid_line:
                res_solids.extend([grid_line])
            else:
                print("Cannot find grid line")
            new_doc = cad.Documents.Add()
            doc.CopyObjects(res_solids, new_doc.ModelSpace)
            new_doc.SaveAs(os.path.join(doc.Path, "{}.dwg".format(out_file_name)))
            new_doc.Close(False)


if __name__ == "__main__":
    main()
