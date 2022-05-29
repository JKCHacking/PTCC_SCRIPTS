import os
import shutil
from comtypes import client


class AssemblyClassifier:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        # initializing the Inventor application
        inv_progid = "Inventor.Application"
        try:
            self.inv_app = client.GetActiveObject(inv_progid, dynamic=True)
        except OSError:
            self.inv_app = client.CreateObject(inv_progid, dynamic=True)

    def collect_parts(self, assembly_path):
        assembly = self.inv_app.Documents.Open(assembly_path)
        component_def = assembly.ComponentDefinition
        assembly_folder_name = os.path.splitext(os.path.basename(assembly_path))[0]

        for occurrence in component_def.Occurrences:
            ref_doc_desc = occurrence.ReferencedDocumentDescriptor
            if ref_doc_desc:
                part_path = ref_doc_desc.FullDocumentName
                self.__copy_to_assembly_folder(assembly_folder_name, part_path)
        assembly.Close(True)
        self.__copy_to_assembly_folder(assembly_folder_name, assembly_path)
        print("[AsmClassifier] Created directory for {}".format(assembly_folder_name))
        print("[AsmClassifier] Number of files inside: {}".format(
            len(os.listdir(os.path.join(self.output_dir, assembly_folder_name)))))

    def __copy_to_assembly_folder(self, assembly_folder_name, src):
        landing_folder = os.path.join(self.output_dir, assembly_folder_name)
        if not os.path.exists(landing_folder):
            os.mkdir(landing_folder)
        dest = os.path.join(landing_folder, os.path.basename(src))
        shutil.copyfile(src, dest)
