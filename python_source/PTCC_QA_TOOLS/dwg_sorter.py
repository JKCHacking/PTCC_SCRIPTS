import os
import tkinter
from tkinter.filedialog import askopenfilename
from comtypes import client
from comtypes import COMError
from comtypes import automation


class DwgSorter:
    def __init__(self, cad_app, doc):
        self.cad_app = cad_app
        self.doc = doc
        self.grid_block = None

    def get_grid_block(self):
        try:
            self.doc.SelectionSets.Item("SELECT GRID").Delete()
        except COMError:
            pass
        selection_set = self.doc.SelectionSets.Add("SELECT GRID")
        selection_set.SelectOnScreen(automation.VARIANT([0]), automation.VARIANT(["INSERT"]))
        self.grid_block = selection_set.Item(0)

    @staticmethod
    def get_objs_by_ci(objs, ic):
        ci_objs = []
        for obj in objs:
            if obj.TrueColor.ColorIndex == ic:
                ci_objs.append(obj)
        return ci_objs

    @staticmethod
    def get_objs_by_layer(objs, layer):
        layer_objs = []
        for obj in objs:
            if obj.Layer == layer:
                layer_objs.append(obj)
        return layer_objs

    def get_layers(self):
        return self.doc.Layers

    @staticmethod
    def get_color_indexes(objs):
        ac_color_method_by_aci = 195
        ac_color_method_by_rgb = 194
        color_indexes = []
        for obj in objs:
            color_index = obj.TrueColor.ColorIndex
            if (obj.TrueColor.ColorMethod == ac_color_method_by_aci or
                    obj.TrueColor.ColorMethod == ac_color_method_by_rgb) and color_index not in color_indexes:
                color_indexes.append(color_index)
        return color_indexes

    def export_objs_to_dwg(self, objs, file_name):
        new_doc = self.cad_app.Documents.Add()
        self.doc.CopyObjects(objs, new_doc.ModelSpace)
        new_doc.SaveAs(os.path.join(self.doc.Path, "{}.dwg".format(file_name)))
        new_doc.Close(False)

    def export_by_color(self, objs):
        color_indexes = self.get_color_indexes(objs)
        for ci in color_indexes:
            objs_ci = self.get_objs_by_ci(objs, ci)
            out_filename = ci
            if self.grid_block:
                objs_ci.extend([self.grid_block])
            else:
                print("Cannot find grid line")
            self.export_objs_to_dwg(objs_ci, out_filename)

    def export_by_layer(self, objs):
        layers = self.get_layers()
        for layer in layers:
            layer_name = layer.Name
            objs_layer = self.get_objs_by_layer(objs, layer_name)
            out_filename = layer_name
            if self.grid_block:
                objs_layer.extend([self.grid_block])
            else:
                print("Cannot find grid line")
            self.export_objs_to_dwg(objs_layer, out_filename)


def get_objects(doc, obj_name):
    objs = []
    for obj in doc.ModelSpace:
        if obj.ObjectName.lower() == obj_name:
            objs.append(obj)
    return objs


if __name__ == "__main__":
    tkinter.Tk().withdraw()
    dwg_path = askopenfilename(title="Select the DWG", filetypes=[("DWG Files", ".dwg")])
    if dwg_path:
        cad_app = client.GetActiveObject("BricscadApp.AcadApplication")
        doc = cad_app.Documents.Open(dwg_path)
        print("Getting objects...")
        objs = get_objects(doc, "acdb3dsolid")

        sorter = DwgSorter(cad_app, doc)
        print("Getting grid block...")
        sorter.get_grid_block()
        print("Exporting by color...")
        sorter.export_by_color(objs)
        print("Exporting by layer...")
        sorter.export_by_layer(objs)
