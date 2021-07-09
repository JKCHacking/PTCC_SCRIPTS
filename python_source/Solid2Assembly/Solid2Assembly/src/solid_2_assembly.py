import os
from comtypes import client


class Solid2Assembly:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        # initializing the Inventor application
        inv_progid = "Inventor.Application"
        try:
            self.inv_app = client.GetActiveObject(inv_progid, dynamic=True)
        except OSError:
            self.inv_app = client.CreateObject(inv_progid, dynamic=True)

    def merge_to_assembly(self, file_input):
        if file_input.endswith(".ipt") or file_input.endswith(".iam"):
            part_fn_list = []
            doc = self.inv_app.Documents.Open(file_input)
            component_definition = doc.ComponentDefinition
            solid_bodies = component_definition.SurfaceBodies
            print("[SOLID2ASSEMBLY:merge_to_assembly]Number of Solids: {}".format(solid_bodies.Count))
            for solid_body in solid_bodies:
                part_fn = self.__create_new_part(solid_body, file_input)
                part_fn_list.append(part_fn)
            self.__create_new_assembly(part_fn_list, file_input)
            doc.Close(True)

    def __create_new_part(self, solid_body, file_input):
        solid_name = solid_body.Name
        part_file_name = "{}.ipt".format(solid_name)
        sub_folder_name = "{}".format(os.path.basename(file_input).split(".")[0])
        part_full_path = os.path.join(self.output_folder, sub_folder_name, part_file_name)
        k_part_document_object = 12290
        part_doc = self.inv_app.Documents.Add(k_part_document_object,
                                              self.inv_app.FileManager.GetTemplateFile(k_part_document_object))
        # add the solid as non parametric base feature
        part_doc.ComponentDefinition.Features.NonParametricBaseFeatures.Add(solid_body)
        part_doc.SaveAs(part_full_path, True)
        part_doc.Close(True)
        return part_full_path

    def __create_new_assembly(self, part_fn_list, file_input):
        assembly_file_name = "{}.iam".format(os.path.basename(file_input).split(".")[0])
        sub_folder_name = "{}".format(os.path.basename(file_input).split(".")[0])
        assembly_full_path = os.path.join(self.output_folder, sub_folder_name, assembly_file_name)
        k_assembly_document_object = 12291
        asm_doc = self.inv_app.Documents.Add(k_assembly_document_object,
                                             self.inv_app.FileManager.GetTemplateFile(k_assembly_document_object))
        for part_file_name in part_fn_list:
            matrix = self.inv_app.TransientGeometry.CreateMatrix()
            asm_doc.ComponentDefinition.Occurrences.Add(part_file_name, matrix)
        asm_doc.SaveAs(assembly_full_path, True)
        asm_doc.Close(True)
        print("[SOLID2ASSEMBLY:create_new_assembly]Assembly file created: {}".format(assembly_full_path))
