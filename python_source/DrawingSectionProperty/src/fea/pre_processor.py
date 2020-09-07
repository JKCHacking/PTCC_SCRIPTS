import ezdxf


class PreProcessor:
    def __init__(self):
        pass

    def create_geometry(self, file_fp):
        '''
            creates the geometry of each profile inside the drawing file
        '''
        geometry_list = []
        drawing_file = ezdxf.readfile(file_fp)
        mod_space = drawing_file.modelspace()
        for ent in mod_space:
            if ent.dxftype() == "LWPOLYLINE":
                print(ent.dxf.handle)
                for sub_ent in ent.virtual_entities():
                    print(sub_ent.dxftype())
        return geometry_list

    def create_mesh(self, mesh_size):
        '''
            creates the mesh of each geometry inside the drawing file
        '''
        pass

    def create_materials(self, material_list):
        pass