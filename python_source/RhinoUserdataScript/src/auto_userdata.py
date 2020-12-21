import rhinoscriptsyntax as rs


NOT_APPLICABLE = "N/A"
ROUND_PRECISION = rs.UnitDistanceDisplayPrecision()
UNIT = rs.UnitSystemName(abbreviate=True)

LAYER_COMPONENT_DATA = {
    "stainless_steel": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "mirror polished",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "SS{count:03d}",
        "type": "Sheet",
        "desc": "3mm thick stainless steel folded sheet"
    },
    "stainless_steel_brackets": {
        "mat_code": "204",
        "finish_code": "44",
        "coating_system": "no finish",
        "material": "1.4404 - S235",
        "density": 8000,  # densities in kg/m^3
        "file_name": "BR001",
        "type": "Sheet",
        "desc": "3mm thick stainless steel folded sheet"
    },
    "alu-profile": {
        "mat_code": "302",
        "finish_code": "51",
        "coating_system": "anodized",
        "material": "EN AW 5005 H14",
        "density": 2712,  # densities in kg/m^3
        "file_name": "AB{count:03d}",
        "type": "Profile",
        "desc": "aluminum block"
    },
    "gasket": {
        "mat_code": "702",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": NOT_APPLICABLE,
        "density": 70,  # densities in kg/m^3
        "file_name": "EP{count:03d}",
        "type": "Gasket",
        "desc": "EPDM gasket"
    },
    "insulation": {
        "mat_code": "620",
        "finish_code": "00",
        "coating_system": "no finish",
        "material": NOT_APPLICABLE,
        "density": 70,  # densities in kg/m^3
        "file_name": "MW{count:03d}",
        "type": "Insulation",
        "desc": "50mm thick insulation"
    },
}


def set_userdata():
    for layer_name in LAYER_COMPONENT_DATA:
        objs = rs.ObjectsByLayer(layer_name)
        for i, obj in enumerate(objs):
            count = i + 1
            walltype = get_walltype(obj)
            glass_build_up = get_glass_build_up(obj)
            mat_code = get_material_code(obj, layer_name)
            fin_code = get_finish_code(obj, layer_name)
            coating_sys = get_coating_system(obj, layer_name)
            uval = get_u_value(obj)
            accval = get_acc_value(obj)
            mat = get_material(obj, layer_name)
            manufacturer = get_manufacturer(obj)
            area = get_area(obj)
            weight = get_weight(obj, layer_name)
            dim = get_dimension(obj)
            name = get_name(obj, layer_name, count)
            type = get_type(obj, layer_name)
            desc = get_description(obj, layer_name)

            rs.SetUserText(obj, "Walltype", walltype)
            rs.SetUserText(obj, "GlassBuildUp", glass_build_up)
            rs.SetUserText(obj, "MaterialCode", mat_code)
            rs.SetUserText(obj, "FinishCode", fin_code)
            rs.SetUserText(obj, "CoatingSystem", coating_sys)
            rs.SetUserText(obj, "UValue", uval)
            rs.SetUserText(obj, "AccousticValue", accval)
            rs.SetUserText(obj, "Material", mat)
            rs.SetUserText(obj, "Manufacturer", manufacturer)
            rs.SetUserText(obj, "Area", area)
            rs.SetUserText(obj, "Weight", weight)
            rs.SetUserText(obj, "Dimension", dim)
            rs.SetUserText(obj, "Name", name)
            rs.SetUserText(obj, "Type", type)
            rs.SetUserText(obj, "Description", desc)

            if layer_name == "alu-profile":
                ext_com = get_extrusion_company(obj)
                die_num = get_die_number(obj)
                alloy_temp = get_alloy_temper(obj)
                rs.SetUserText(obj, "ExtrusionCompany", ext_com)
                rs.SetUserText(obj, "DieNumber", die_num)
                rs.SetUserText(obj, "AlloyTemper", alloy_temp)


def get_walltype(obj):
    return "WT3C"


def get_glass_build_up(obj):
    return NOT_APPLICABLE


def get_material_code(obj, material):
    mat_code = LAYER_COMPONENT_DATA[material]["mat_code"]
    return mat_code


def get_finish_code(obj, material):
    fin_code = LAYER_COMPONENT_DATA[material]["finish_code"]
    return fin_code


def get_coating_system(obj, material):
    coating_system = LAYER_COMPONENT_DATA[material]["coating_system"]
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
    material_name = LAYER_COMPONENT_DATA[material]["material"]
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
        rs.SelectObject(obj)
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
                m = s_vol * LAYER_COMPONENT_DATA[material]["density"]
            else:
                print("Warning: Cannot obtain surface area.")
        else:
            print("Warning: Polysurface is not closed {}".format(obj))
    except Exception as e:
        rs.SelectObject(obj)
        print(e)

    return str(round(m, ROUND_PRECISION)) + " kg"


def get_dimension(obj):
    bb = rs.BoundingBox(obj)
    length = round(bb[3].DistanceTo(bb[0]), ROUND_PRECISION)  # YL
    width = round(bb[1].DistanceTo(bb[0]), ROUND_PRECISION)  # XL
    height = round(bb[4].DistanceTo(bb[0]), ROUND_PRECISION)  # ZL
    return "{}X{}X{} mm".format(length, width, height)


def get_name(obj, material, count):
    filename = LAYER_COMPONENT_DATA[material]["file_name"].format(count=count)
    name = "2MR-SEE-POD-EWL-F03-L06-WT3C-{filename}-R00"
    name = name.format(filename=filename)
    return name


def get_type(obj, material):
    type = LAYER_COMPONENT_DATA[material]["type"]
    return type


def get_description(obj, material):
    desc = LAYER_COMPONENT_DATA[material]["desc"]
    return desc


if __name__ == "__main__":
    set_userdata()
