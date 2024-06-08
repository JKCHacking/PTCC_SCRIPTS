import rhinoscriptsyntax as rs


NOT_APPLICABLE = "-"
TBD = "TBD"
ROUND_PRECISION = rs.UnitDistanceDisplayPrecision()
UNIT = rs.UnitSystemName(abbreviate=True)

BLOCK_REPRESENTATIVES = ["sheet", "stainless_steel_brackets", "gasket", "insulation", "flashing"]

LAYERS_MATERIAL_DATA = {
    "sheet": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "mirror polished",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "SS{count:03d}",
        "type": "SS Sheet",
        "apvorlage": "V-VA09",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "2"
    },
    "stainless_steel_brackets": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "BR{count:03d}",
        "type": "SS Bracket",
        "apvorlage": "V-VA04",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "1"
    },
    "flashing": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "FL{count:03d}",
        "type": "Sheet",
        "apvorlage": "",
        "desc": "2mm thick stainless steel folded sheet",
        "obj_name_num": "1"
    },
    "alu-profile": {
        "name": "{name}",
        "mat_code": "302",
        "finish_code": "51",
        "coating_system": "anodized",
        "material": TBD,
        "density": 2712,  # densities in kg/m^3
        "file_name": "AP{count:03d}",
        "type": "AL Profile Cut",
        "apvorlage": "V-AL35",
        "desc": "aluminum profile",
        "obj_name_num": "6"
    },
    "alu-block": {
        "mat_code": "302",
        "finish_code": "51",
        "coating_system": "anodized",
        "material": TBD,
        "density": 2712,  # densities in kg/m^3
        "file_name": "AB{count:03d}",
        "type": "AL Profile Cut",
        "apvorlage": "V-AL35",
        "desc": "aluminum block",
        "obj_name_num": "7"
    },
    "gasket": {
        "mat_code": "702",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 70,  # densities in kg/m^3
        "file_name": "EP{count:03d}",
        "type": "Gasket Cut",
        "apvorlage": "V-DP01",
        "desc": "EPDM gasket",
        "obj_name_num": "1"
    },
    "insulation": {
        "mat_code": "620",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 70,  # densities in kg/m^3
        "file_name": "MW{count:03d}",
        "type": "Insulation Cut",
        "apvorlage": "V-DS01",
        "desc": "50mm thick insulation",
        "obj_name_num": "8"
    },
    "rib": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "RB{count:03d}",
        "type": "SS Sheet",
        "apvorlage": "V-VA09",
        "desc": "4mm thick stainless steel sheet",
        "obj_name_num": "5"
    },
    "rib-plate": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "RP{count:03d}",
        "type": "SS Special Part",
        "apvorlage": "V-VA14",
        "desc": "5mm thick stainless steel plate",
        "obj_name_num": "4"
    },
    "splice": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "mirror polished",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "SP{count:03d}",
        "type": "SS Sheet",
        "apvorlage": "V-VA09",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "3"
    },
    "washer": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": TBD,
        "density": 8000,  # densities in kg/m^3
        "file_name": "WS{count:03d}",
        "type": "SS Special Part",
        "apvorlage": "V-VA14",
        "desc": "3mm thick stainless steel washer",
        "obj_name_num": "2"
    }
}


def iter_objects():
    # getting the list of block names
    block_names = rs.BlockNames(True)
    # get only the block names that starts with "D"
    interest_block_names = [block_name for block_name in block_names if block_name.startswith("D")]
    # interest_block_names = rs.GetObjects("Select the objects to add metadata.")

    for blk_name in interest_block_names:
        print("BlockName: {}".format(blk_name))
        # getting a block object from a block name
        child_object_list = rs.BlockObjects(blk_name)
        representative_layer = ""
        # getting list of objects that makes up the block.
        for child_object in child_object_list:
            layer_name = rs.ObjectLayer(child_object).split("::")[-1]
            if layer_name in LAYERS_MATERIAL_DATA:
                # sets the object name according to layer
                set_objectname(child_object, blk_name, layer_name)
                set_userdata(child_object, blk_name, layer_name)
            if layer_name in BLOCK_REPRESENTATIVES and representative_layer == "":
                representative_layer = layer_name
        block_objects = rs.BlockInstances(blk_name)
        for block_object in block_objects:
            set_objectname(block_object, blk_name, representative_layer)
            set_userdata(block_object, blk_name, representative_layer)

    # for obj in interest_block_names:
    #     layer = rs.ObjectLayer(obj).split("::")[-1]
    #     set_userdata(obj, rs.ObjectName(obj), layer)


def set_userdata(obj_id, name, layer_name):
    name = get_name(obj_id, name, layer_name)
    weight = get_weight(obj_id, name, layer_name)
    uval = get_u_value()
    accval = get_acc_value()
    area = get_area(obj_id, name)
    manufacturer = get_manufacturer()
    glass_build_up = get_glass_build_up()
    type = get_type(layer_name)
    fin_code = get_finish_code(layer_name)
    coating_sys = get_coating_system()
    location = get_location()
    mat_code = get_material_code(layer_name)
    mat = get_material(obj_id, layer_name)
    code = get_code()
    dim = get_dimension(obj_id)
    desc = get_description(layer_name)
    apvorlage = get_apvorlage(layer_name)

    rs.SetUserText(obj_id, "Name", name)
    rs.SetUserText(obj_id, "Weight", weight)
    rs.SetUserText(obj_id, "UValue", uval)
    rs.SetUserText(obj_id, "AccousticValue", accval)
    rs.SetUserText(obj_id, "Area", area)
    rs.SetUserText(obj_id, "Manufacturer", manufacturer)
    rs.SetUserText(obj_id, "GlassBuildUp", glass_build_up)
    rs.SetUserText(obj_id, "Type", type)
    rs.SetUserText(obj_id, "FinishCode", fin_code)
    rs.SetUserText(obj_id, "CoatingSystem", coating_sys)
    rs.SetUserText(obj_id, "Location", location)
    rs.SetUserText(obj_id, "MaterialCode", mat_code)
    rs.SetUserText(obj_id, "Material", mat)
    rs.SetUserText(obj_id, "Code", code)
    rs.SetUserText(obj_id, "Dimension", dim)
    rs.SetUserText(obj_id, "Description", desc)
    rs.SetUserText(obj_id, "APVorlage", apvorlage)

    if layer_name == "alu-profile":
        ext_com = get_extrusion_company()
        die_num = get_die_number()
        alloy_temp = get_alloy_temper()
        rs.SetUserText(obj_id, "ExtrusionCompany", ext_com)
        rs.SetUserText(obj_id, "DieNumber", die_num)
        rs.SetUserText(obj_id, "AlloyTemper", alloy_temp)


def set_objectname(obj, block_name, layer_name):
    object_name = get_name(obj, block_name, layer_name)
    rs.ObjectName(obj, object_name)
    print("\tObject Name: {}".format(object_name))


def get_name(obj, name, layer_name):
    # if its not a block instance you have to construct the name
    if not rs.IsBlockInstance(obj):
        block_name_split = name.split("-")
        prefix = "{}{}{}".format(block_name_split[0][0:-2],
                                 LAYERS_MATERIAL_DATA[layer_name]["obj_name_num"],
                                 block_name_split[0][-1])
        block_name_split[0] = prefix
        name = "-".join(block_name_split)
    return name


def get_weight(obj, block_name,  material):
    print("Getting Weight...")
    if rs.IsBlockInstance(obj):
        m = get_block_weight(block_name)
    else:
        m = get_component_weight(obj, material)
    if not m:
        m = 0
    return str(round(m, ROUND_PRECISION)) + " kg"


def get_block_weight(block_name):
    m = 0
    # get all the child object within the block instance
    block_object = rs.BlockObjects(block_name)
    for child_object in block_object:
        child_material_name = rs.ObjectLayer(child_object).split("::")[-1]
        if rs.IsPolysurface(child_object) and rs.IsPolysurfaceClosed(child_object) and \
                child_material_name in LAYERS_MATERIAL_DATA:
            s_vol = rs.SurfaceVolume(child_object)
            if s_vol:
                s_vol = s_vol[0]
                if UNIT == "mm":
                    s_vol = s_vol * 1e-09
                m += s_vol * LAYERS_MATERIAL_DATA[child_material_name]["density"]
            else:
                print("Warning: Cannot obtain surface Volume. {}".format(rs.ObjectName(child_object)))
        else:
            print("Warning: Object is not Polysurface or not closed. {}".format(rs.ObjectName(child_object)))
    return m


def get_component_weight(component_obj, material):
    m = 0
    if rs.IsPolysurface(component_obj) and rs.IsPolysurfaceClosed(component_obj):
        s_vol = rs.SurfaceVolume(component_obj)
        if s_vol:
            s_vol = s_vol[0]
            if UNIT == "mm":
                s_vol = s_vol * 1e-09
            m = s_vol * LAYERS_MATERIAL_DATA[material]["density"]
        else:
            print("Warning: Cannot obtain surface Volume. {}".format(rs.ObjectName(component_obj)))
    else:
        print("Warning: Object is not Polysurface or not closed. {}".format(rs.ObjectName(component_obj)))
    return m


def get_u_value():
    return NOT_APPLICABLE


def get_acc_value():
    return NOT_APPLICABLE


def get_area(obj, block_name):
    print("Getting Area...")
    if rs.IsBlockInstance(obj):
        area = get_block_area(block_name)
    else:
        area = get_component_area(obj)
    if not area:
        area = 0
    return str(round(area, ROUND_PRECISION)) + " m^2"


def get_block_area(block_name):
    area = 0
    block_obj = rs.BlockObjects(block_name)
    for child_obj in block_obj:
        child_material_name = rs.ObjectLayer(child_obj).split("::")[-1]
        if rs.IsPolysurface(child_obj) and rs.IsPolysurfaceClosed(child_obj) and \
                child_material_name in LAYERS_MATERIAL_DATA:
            area = rs.SurfaceArea(child_obj)
            if area:
                area = area[0]
                if UNIT == "mm":
                    # convert mm^2 to m^2
                    area += area * 1e-06
            else:
                print("Warning: Cannot obtain surface area! {}".format(rs.ObjectName(child_obj)))
        else:
            print("Warning: Object is not Polysurface or not closed. {}".format(rs.ObjectName(child_obj)))
    return area


def get_component_area(component_obj):
    area = 0
    if rs.IsPolysurface(component_obj) and rs.IsPolysurfaceClosed(component_obj):
        area = rs.SurfaceArea(component_obj)
        if area:
            area = area[0]
            if UNIT == "mm":
                # convert mm^2 to m^2
                area = area * 1e-06
        else:
            print("Warning: Cannot obtain surface area! {}".format(rs.ObjectName(component_obj)))
    else:
        print("Warning: Object is not Polysurface or not closed. {}".format(rs.ObjectName(component_obj)))
    return area


def get_extrusion_company():
    return TBD


def get_die_number():
    return NOT_APPLICABLE


def get_alloy_temper():
    return TBD


def get_manufacturer():
    return TBD


def get_glass_build_up():
    return NOT_APPLICABLE


def get_type(material):
    type = LAYERS_MATERIAL_DATA[material]["type"]
    return type


def get_finish_code(material):
    fin_code = LAYERS_MATERIAL_DATA[material]["finish_code"]
    return fin_code


def get_coating_system():
    # coating_system = LAYERS_MATERIAL_DATA[material]["coating_system"]
    # return coating_system
    return TBD


def get_location():
    return NOT_APPLICABLE


def get_material_code(material):
    mat_code = LAYERS_MATERIAL_DATA[material]["mat_code"]
    return mat_code


def get_material(obj, material):
    material_name = LAYERS_MATERIAL_DATA[material]["material"]
    return material_name


def get_code():
    return TBD


def get_dimension(obj):
    bb = rs.BoundingBox(obj)
    length = round(bb[3].DistanceTo(bb[0]), ROUND_PRECISION)  # YL
    width = round(bb[1].DistanceTo(bb[0]), ROUND_PRECISION)  # XL
    height = round(bb[4].DistanceTo(bb[0]), ROUND_PRECISION)  # ZL
    return "{}X{}X{} mm".format(length, width, height)


def get_description(material):
    desc = LAYERS_MATERIAL_DATA[material]["desc"]
    return desc


def get_apvorlage(material):
    apvorlage = LAYERS_MATERIAL_DATA[material]["apvorlage"]
    return apvorlage


if __name__ == "__main__":
    iter_objects()
