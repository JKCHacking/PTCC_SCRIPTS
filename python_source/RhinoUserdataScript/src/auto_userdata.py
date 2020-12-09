import rhinoscriptsyntax as rs


NOT_APPLICABLE = "N/A"
ROUND_PRECISION = rs.UnitDistanceDisplayPrecision()
UNIT = rs.UnitSystemName(abbreviate=True)


def automate_userdata():
    layers = [
        "stainless_steel",
        "stainless_steel_bracket",
        "alu-profile",
        "gasket",
        "insulation"
    ]

    for layer in layers:
        objs = rs.ObjectsByLayer(layer)
        for i, obj in enumerate(objs):
            count = i + 1
            walltype = set_walltype(obj)
            glass_build_up = set_glass_build_up(obj)
            mat_code = set_material_code(obj, layer)
            fin_code = set_finish_code(obj, layer)
            coating_sys = set_coating_system(obj, layer)
            uval = set_u_value(obj)
            accval = set_acc_value(obj)
            mat = set_material(obj, layer)
            manufacturer = set_manufacturer(obj)
            area = set_area(obj)
            weight = set_weight(obj, layer)
            dim = set_dimension(obj)
            name = set_name(obj, layer, count)
            type = set_type(obj, layer)
            desc = set_description(obj, layer)

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
                ext_com = set_extrusion_company(obj)
                die_num = set_die_number(obj)
                alloy_temp = set_alloy_temper(obj)
                rs.SetUserText(obj, "ExtrusionCompany", ext_com)
                rs.SetUserText(obj, "DieNumber", die_num)
                rs.SetUserText(obj, "AlloyTemper", alloy_temp)


def set_walltype(obj):
    return "WT3C"


def set_glass_build_up(obj):
    return NOT_APPLICABLE


def set_material_code(obj, material):
    material_codes = {
        "stainless_steel": "204",
        "stainless_steel_bracket": "204",
        "gasket": "702",
        "alu-profile": "302",
        "insulation": "620"
    }
    if material in material_codes:
        mat_code = material_codes[material]
    else:
        mat_code = NOT_APPLICABLE
    return mat_code


def set_finish_code(obj, material):
    finish_codes = {
        "stainless_steel": "44",
        "alumninum": "51",
    }

    if material in finish_codes:
        fin_code = finish_codes[material]
    else:
        fin_code = "00"

    return fin_code


def set_coating_system(obj, material):
    coating_system_dict = {
        "stainless_steel": "mirror polished",
        "aluminum": "anodized"
    }
    if material in coating_system_dict:
        coating_system = coating_system_dict[material]
    else:
        coating_system = "no finish"
    return coating_system


def set_extrusion_company(obj):
    return "to be determined..."


def set_die_number(obj):
    return NOT_APPLICABLE


def set_alloy_temper(obj):
    return "AA 5005"


def set_u_value(obj):
    return NOT_APPLICABLE


def set_acc_value(obj):
    return NOT_APPLICABLE


def set_material(obj, material):
    material_names = {
        "stainless_steel": "1.4404 - S235",
        "stainless_steel_bracket": "1.4404 - S235",
        "alu-profile": "EN AW 5005 H14"
    }

    if material in material_names:
        material_name = material_names[material]
    else:
        material_name = NOT_APPLICABLE
    return material_name


def set_manufacturer(obj):
    return "to be determined..."


def set_area(obj):
    area = rs.SurfaceArea(obj)[0]
    if UNIT == "mm":
        # convert mm^2 to m^2
        area = area * 1e-06
    return str(round(area, ROUND_PRECISION)) + " m^2"


def set_weight(obj, material):
    # densities in kg/m^3
    mat_den = {
        "stainless_steel": 8000,
        "stainless_steel_bracket": 8000,
        "fixing": 8000,
        "alu-profile": 2712,
        "gasket": 70,
        "insulation": 70
    }

    s_vol = rs.SurfaceVolume(obj)[0]
    if s_vol:
        if UNIT == "mm":
            s_vol = s_vol * 1e-09
        m = s_vol * mat_den[material]
    else:
        m = 0
    return str(round(m, ROUND_PRECISION)) + " kg"


def set_dimension(obj):
    bb = rs.BoundingBox(obj)
    length = round(bb[3].DistanceTo(bb[0]), ROUND_PRECISION)  # YL
    width = round(bb[1].DistanceTo(bb[0]), ROUND_PRECISION)  # XL
    height = round(bb[4].DistanceTo(bb[0]), ROUND_PRECISION)  # ZL
    return "{}X{}X{} mm".format(length, width, height)


def set_name(obj, material, count):
    name = "2MR-SEE-POD-EWL-AXX-L06-WT3C-{filename}-R00"
    filename_temp_dict = {
        "stainless_steel": "SS{count:03d}",
        "stainless_steel_bracket": "BR001",
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


def set_type(obj, material):
    type_dict = {
        "stainless_steel": "Sheet",
        "stainless_steel_bracket": "Sheet",
        "alu-profile": "Profile",
        "gasket": "Gasket",
        "insulation": "Insulation"
    }

    if material in type_dict:
        type = type_dict[material]
    else:
        type = NOT_APPLICABLE
    return type


def set_description(obj, material):
    desc_dict = {
        "stainless_steel": "3mm thick stainless steel folded sheet",
        "stainless_steel_bracket": "3mm thick stainless steel folded sheet",
        "gasket": "EPDM gasket",
        "al-profile": "aluminum block",
        "insulation": "50mm thick insulation"
    }

    if material in desc_dict:
        desc = desc_dict[material]
    else:
        desc = NOT_APPLICABLE

    return desc


if __name__ == "__main__":
    automate_userdata()
