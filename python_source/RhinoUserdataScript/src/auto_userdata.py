import rhinoscriptsyntax as rs


NOT_APPLICABLE = "N/A"
ROUND_PRECISION = rs.UnitDistanceDisplayPrecision()
UNIT = rs.UnitSystemName(abbreviate=True)


def set_userdata():
    layers = [
        "stainless_steel",
        "stainless_steel_brackets",
        "alu-profile",
        "gasket",
        # "insulation"
    ]

    for layer in layers:
        objs = rs.ObjectsByLayer(layer)
        for i, obj in enumerate(objs):
            count = i + 1
            walltype = get_walltype(obj)
            glass_build_up = get_glass_build_up(obj)
            mat_code = get_material_code(obj, layer)
            fin_code = get_finish_code(obj, layer)
            coating_sys = get_coating_system(obj, layer)
            uval = get_u_value(obj)
            accval = get_acc_value(obj)
            mat = get_material(obj, layer)
            manufacturer = get_manufacturer(obj)
            area = get_area(obj)
            weight = get_weight(obj, layer)
            dim = get_dimension(obj)
            name = get_name(obj, layer, count)
            type = get_type(obj, layer)
            desc = get_description(obj, layer)

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

            if layer == "alu-profile":
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
    material_codes = {
        "stainless_steel": "204",
        "stainless_steel_brackets": "204",
        "gasket": "702",
        "alu-profile": "302",
        "insulation": "620"
    }
    if material in material_codes:
        mat_code = material_codes[material]
    else:
        mat_code = NOT_APPLICABLE
    return mat_code


def get_finish_code(obj, material):
    finish_codes = {
        "stainless_steel": "44",
        "alumninum": "51",
    }

    if material in finish_codes:
        fin_code = finish_codes[material]
    else:
        fin_code = "00"

    return fin_code


def get_coating_system(obj, material):
    coating_system_dict = {
        "stainless_steel": "mirror polished",
        "aluminum": "anodized"
    }
    if material in coating_system_dict:
        coating_system = coating_system_dict[material]
    else:
        coating_system = "no finish"
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
    material_names = {
        "stainless_steel": "1.4404 - S235",
        "stainless_steel_brackets": "1.4404 - S235",
        "alu-profile": "EN AW 5005 H14"
    }

    if material in material_names:
        material_name = material_names[material]
    else:
        material_name = NOT_APPLICABLE
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
    # densities in kg/m^3
    mat_den = {
        "stainless_steel": 8000,
        "stainless_steel_brackets": 8000,
        "fixing": 8000,
        "alu-profile": 2712,
        "gasket": 70,
        "insulation": 70
    }
    m = 0
    try:
        if rs.IsPolysurfaceClosed(obj):
            s_vol = rs.SurfaceVolume(obj)[0]
            if s_vol:
                if UNIT == "mm":
                    s_vol = s_vol * 1e-09
                m = s_vol * mat_den[material]
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
    name = "2MR-SEE-POD-EWL-F03-L06-WT3C-{filename}-R00"
    filename_temp_dict = {
        "stainless_steel": "SS{count:03d}",
        "stainless_steel_brackets": "BR001",
        "gasket": "EP{count:03d}",
        "alu-profile": "AB{count:03d}",
        "insulation": "MW{count:03d}"
    }

    if material in filename_temp_dict:
        filename = filename_temp_dict[material].format(count=count)
        name = name.format(filename=filename)
    else:
        name = NOT_APPLICABLE
    return name


def get_type(obj, material):
    type_dict = {
        "stainless_steel": "Sheet",
        "stainless_steel_brackets": "Sheet",
        "alu-profile": "Profile",
        "gasket": "Gasket",
        "insulation": "Insulation"
    }

    if material in type_dict:
        type = type_dict[material]
    else:
        type = NOT_APPLICABLE
    return type


def get_description(obj, material):
    desc_dict = {
        "stainless_steel": "3mm thick stainless steel folded sheet",
        "stainless_steel_brackets": "3mm thick stainless steel folded sheet",
        "gasket": "EPDM gasket",
        "alu-profile": "aluminum block",
        "insulation": "50mm thick insulation"
    }

    if material in desc_dict:
        desc = desc_dict[material]
    else:
        desc = NOT_APPLICABLE

    return desc


if __name__ == "__main__":
    set_userdata()
