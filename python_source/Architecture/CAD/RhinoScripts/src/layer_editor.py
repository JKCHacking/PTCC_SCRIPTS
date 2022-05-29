import rhinoscriptsyntax as rs
from scriptcontext import doc


def rename_layers():
    layer_subname = rs.GetString("Sub-name of layer to rename")
    new_layer_subname = rs.GetString("New layer subname")
    matched_layers = [layer for layer in doc.Layers if layer_subname in layer.Name]
    for matched_layer in matched_layers:
        new_full_layer_name = matched_layer.Name.replace(layer_subname, new_layer_subname)
        print("Layer name: {}\nReplaced with: {}\n".format(matched_layer.Name, new_full_layer_name))
        matched_layer.Name = new_full_layer_name
        matched_layer.CommitChanges()


if __name__ == "__main__":
    rename_layers()
