import rhinoscriptsyntax as rs


NOT_APPLICABLE = "N/A"
ROUND_PRECISION = rs.UnitDistanceDisplayPrecision()
UNIT = rs.UnitSystemName(abbreviate=True)

BLOCKS = [
    "D4301-F2000",
    "D4301-F2001",
    "D4301-F2002",
    "D4301-F2003",
    "D4301-F2004",
    "D4301-F2005",
    "D4301-F2006",
    "D4301-F2007",
    "D4301-F2008",
    "D4301-F2009",
    "D4301-F2010",
    "D4301-G2003",
    "D4301-G2004",
    "D4301-G2005",
    "D4301-G2006",
    "D4301-G2007",
    "D4301-G2008",
    "D4301-G2009",
    "D4301-G2010",
    "D4301-G2011",
    "D4302-F2011",
    "D4302-F2012",
    "D4302-F2013",
    "D4302-F2014",
    "D4302-G2000",
    "D4302-G2001",
    "D4302-G2002",
    "D4322-F2011",
    "D4322-F2012",
    "D4322-F2013",
    "D4322-F2014",
    "D4322-G2000",
    "D4322-G2001",
    "D4322-G2002",
]

LAYERS_MATERIAL_DATA = {
    "sheet": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "mirror polished",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "SS{count:03d}",
        "type": "Sheet",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "2"
    },
    "stainless_steel_brackets": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "no finish",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "BR001",
        "type": "Sheet",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "2"
    },
    "alu-profile": {
        "mat_code": "302",
        "finish_code": "51",
        "coating_system": "anodized",
        "material": "EN AW 5005 H14",
        "density": 2712,  # densities in kg/m^3
        "file_name": "AB{count:03d}",
        "type": "Profile",
        "desc": "aluminum block",
        "obj_name_num": "6"
    },
    "gasket": {
        "mat_code": "702",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": NOT_APPLICABLE,
        "density": 70,  # densities in kg/m^3
        "file_name": "EP{count:03d}",
        "type": "Gasket",
        "desc": "EPDM gasket",
        "obj_name_num": "1"
    },
    "insulation": {
        "mat_code": "620",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": NOT_APPLICABLE,
        "density": 70,  # densities in kg/m^3
        "file_name": "MW{count:03d}",
        "type": "Insulation",
        "desc": "50mm thick insulation",
        "obj_name_num": "7"
    },
    "rib": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "RB{count:03d}",
        "type": "Sheet",
        "desc": "4mm thick stainless steel sheet",
        "obj_name_num": "5"
    },
    "rib-plate": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "RP{count:03d}",
        "type": "Plate",
        "desc": "5mm thick stainless steel plate",
        "obj_name_num": "4"
    },
    "splice": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "mirror polished",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "SP{count:03d}",
        "type": "Sheet",
        "desc": "3mm thick stainless steel folded sheet",
        "obj_name_num": "3"
    },
    "washer": {
        "mat_code": "204",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "WS{count:03d}",
        "type": "Washer",
        "desc": "3mm thick stainless steel washer",
        "obj_name_num": "1"
    }
}


def iter_objects():
    blk_names = rs.BlockNames(True)
    for blk_name in blk_names:
        if blk_name in BLOCKS:
            blk_obj_ids = rs.BlockObjects(blk_name)
            for blk_obj_id in blk_obj_ids:
                count = 1
                layer_name = rs.ObjectLayer(blk_obj_id)
                if layer_name in LAYERS_MATERIAL_DATA:
                    print("working on object {} under block name: {}".format(blk_obj_id, blk_name))
                    # sets the object name according to layer
                    set_objectname(blk_obj_id, blk_name, layer_name)
                    set_userdata(blk_obj_id, layer_name, count)


def set_userdata(obj_id, layer_name, count):
    walltype = get_walltype(obj_id)
    glass_build_up = get_glass_build_up(obj_id)
    mat_code = get_material_code(obj_id, layer_name)
    fin_code = get_finish_code(obj_id, layer_name)
    coating_sys = get_coating_system(obj_id, layer_name)
    uval = get_u_value(obj_id)
    accval = get_acc_value(obj_id)
    mat = get_material(obj_id, layer_name)
    manufacturer = get_manufacturer(obj_id)
    area = get_area(obj_id)
    weight = get_weight(obj_id, layer_name)
    dim = get_dimension(obj_id)
    name = get_name(obj_id, layer_name, count)
    type = get_type(obj_id, layer_name)
    desc = get_description(obj_id, layer_name)

    rs.SetUserText(obj_id, "Walltype", walltype)
    rs.SetUserText(obj_id, "GlassBuildUp", glass_build_up)
    rs.SetUserText(obj_id, "MaterialCode", mat_code)
    rs.SetUserText(obj_id, "FinishCode", fin_code)
    rs.SetUserText(obj_id, "CoatingSystem", coating_sys)
    rs.SetUserText(obj_id, "UValue", uval)
    rs.SetUserText(obj_id, "AccousticValue", accval)
    rs.SetUserText(obj_id, "Material", mat)
    rs.SetUserText(obj_id, "Manufacturer", manufacturer)
    rs.SetUserText(obj_id, "Area", area)
    rs.SetUserText(obj_id, "Weight", weight)
    rs.SetUserText(obj_id, "Dimension", dim)
    rs.SetUserText(obj_id, "Name", name)
    rs.SetUserText(obj_id, "Type", type)
    rs.SetUserText(obj_id, "Description", desc)

    if layer_name == "alu-profile":
        ext_com = get_extrusion_company(obj_id)
        die_num = get_die_number(obj_id)
        alloy_temp = get_alloy_temper(obj_id)
        rs.SetUserText(obj_id, "ExtrusionCompany", ext_com)
        rs.SetUserText(obj_id, "DieNumber", die_num)
        rs.SetUserText(obj_id, "AlloyTemper", alloy_temp)


def set_objectname(obj, block_name, layer_name):
    block_name_split = block_name.split("-")
    prefix = "{}{}{}".format(block_name_split[0][0:-2],
                             LAYERS_MATERIAL_DATA[layer_name]["obj_name_num"],
                             block_name_split[0][-1])
    block_name_split[0] = prefix
    object_name = "-".join(block_name_split)
    rs.ObjectName(obj, object_name)
    print(object_name)


def get_walltype(obj):
    return "WT3C"


def get_glass_build_up(obj):
    return NOT_APPLICABLE


def get_material_code(obj, material):
    mat_code = LAYERS_MATERIAL_DATA[material]["mat_code"]
    return mat_code


def get_finish_code(obj, material):
    fin_code = LAYERS_MATERIAL_DATA[material]["finish_code"]
    return fin_code


def get_coating_system(obj, material):
    coating_system = LAYERS_MATERIAL_DATA[material]["coating_system"]
    return coating_system


def get_extrusion_company(obj):
    return "to be determined..."


def get_die_number(obj):
    return NOT_APPLICABLE


def get_alloy_temper(obj):
    return "AA 5005"


def get_u_value(obj):
    return NOT_APPLICABLE


def get_acc_value(obj):
    return NOT_APPLICABLE


def get_material(obj, material):
    material_name = LAYERS_MATERIAL_DATA[material]["material"]
    return material_name


def get_manufacturer(obj):
    return "to be determined..."


def get_area(obj):
    area = 0
    try:
        if rs.IsPolysurfaceClosed(obj):
            area = rs.SurfaceArea(obj)[0]
            if area:
                if UNIT == "mm":
                    # convert mm^2 to m^2
                    area = area * 1e-06
            else:
                print("Warning: Cannot obtain surface area!")
        else:
            print("Warning: Polysurface is not closed {}".format(obj))
    except Exception as e:
        print(e)
    # else:
    #     print("Warning: Polysurface is not closed {}".format(obj))
    return str(round(area, ROUND_PRECISION)) + " m^2"


def get_weight(obj, material):
    m = 0
    try:
        if rs.IsPolysurfaceClosed(obj):
            s_vol = rs.SurfaceVolume(obj)[0]
            if s_vol:
                if UNIT == "mm":
                    s_vol = s_vol * 1e-09
                m = s_vol * LAYERS_MATERIAL_DATA[material]["density"]
            else:
                print("Warning: Cannot obtain surface area.")
        else:
            print("Warning: Polysurface is not closed {}".format(obj))
    except Exception as e:
        print(e)

    return str(round(m, ROUND_PRECISION)) + " kg"


def get_dimension(obj):
    bb = rs.BoundingBox(obj)
    length = round(bb[3].DistanceTo(bb[0]), ROUND_PRECISION)  # YL
    width = round(bb[1].DistanceTo(bb[0]), ROUND_PRECISION)  # XL
    height = round(bb[4].DistanceTo(bb[0]), ROUND_PRECISION)  # ZL
    return "{}X{}X{} mm".format(length, width, height)


def get_name(obj, material, count):
    filename = LAYERS_MATERIAL_DATA[material]["file_name"].format(count=count)
    name = "2MR-SEE-POD-EWL-F03-L06-WT3C-{filename}-R00"
    name = name.format(filename=filename)
    return name


def get_type(obj, material):
    type = LAYERS_MATERIAL_DATA[material]["type"]
    return type


def get_description(obj, material):
    desc = LAYERS_MATERIAL_DATA[material]["desc"]
    return desc


if __name__ == "__main__":
    iter_objects()
