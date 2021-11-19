from collections import OrderedDict
import json
import rhinoscriptsyntax as rs

ID_COUNT = 1


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def get_part_quantity(part_id, assembly_id=None):
    count = 0
    part_name = get_specific_part_name(part_id)
    if assembly_id:
        asm_ids = rs.BlockObjects(rs.BlockInstanceName(assembly_id))
        for asm_id in asm_ids:
            if part_name == get_specific_part_name(asm_id):
                count += 1
    else:
        for obj_id in rs.AllObjects():
            if part_name == get_specific_part_name(obj_id):
                count += 1
    return count


def create_desc2(part_name):
    desc2 = ""
    type_dict = {
        "": "",
        "T": "truss",
        "B": "bracing",
        "F": "frame",
        "TC": "topchord",
        "BC": "bottomchord",
        "EX": "extensionpart",
        "DP": "diagonalpart",
        "PR": "profile",
        "CP": "SS-connectionpart",
        "EP": "endpart",
        "VP": "verticalpart",
        "HP": "horizontalpart",
        "STC": "SP-topchord",
        "SBC": "SP-bottomchord",
        "SDP": "SP-diagonalpart",
        "SCP": "SP-SS-connectionpart"
    }
    part_name_ls = part_name.split("-")
    if part_name_ls[1].startswith("S"):
        part_type = type_dict[part_name_ls[1][0:3]]
        part_number = part_name_ls[1][3:]
        desc2 = "{part_type}-{part_number}".format(part_type=part_type, part_number=part_number)
    else:
        if len(part_name_ls) == 4:
            asm_type = type_dict[part_name_ls[2][0]]
            asm_num = part_name_ls[2][1:]
            part_type = type_dict[part_name_ls[3][0:2]]
            part_num = part_name_ls[3][2:]
            desc2 = "{assembly_type}-{assembly_number}-{part_type}-{part_number}".format(
                assembly_type=asm_type,
                assembly_number=asm_num,
                part_type=part_type,
                part_number=part_num
            )
        elif len(part_name_ls) == 3:
            asm_type = type_dict[part_name_ls[2][0]]
            asm_num = part_name_ls[2][1:]
            desc2 = "{assembly_type}-{assembly_number}".format(
                assembly_type=asm_type,
                assembly_number=asm_num
            )
    return desc2


def create_part(u_no,
                s_no,
                i_no,
                desc,
                desc2,
                quantity,
                unit,
                length,
                width,
                height,
                d_no,
                efal,
                child_parts):
    part = OrderedDict([
        ("u_no", u_no),
        ("s_no", s_no),
        ("i_no", i_no),
        ("desc", desc),
        ("desc2", desc2),
        ("quantity", quantity),
        ("unit", unit),
        ("length", round(length, 2)),
        ("width", round(width, 2)),
        ("height", round(height, 2)),
        ("d_no", d_no),
        ("efal", efal),
        ("child_parts", child_parts)
    ])
    return part


def init_part(obj_id, assembly=None):
    part_name = get_specific_part_name(obj_id)
    part = create_part(
        u_no=0,
        s_no=0,
        i_no=rs.GetUserText(obj_id, "06_TEMPLATE_DE"),
        desc=rs.GetUserText(obj_id, "07_TEMPLATE_NAME_DE"),
        desc2=create_desc2(part_name),
        quantity=get_part_quantity(obj_id, assembly),
        unit="Stuck",
        length=float(rs.GetUserText(obj_id, "21_LENGTH")),
        width=float(rs.GetUserText(obj_id, "22_WIDTH")),
        height=float(rs.GetUserText(obj_id, "23_HEIGHT")),
        d_no=part_name,
        efal=[None, "X", "X", None],
        child_parts={}
    )
    return part


def init_raw_part(obj_id):
    part_name = get_specific_part_name(obj_id)
    length = float(rs.GetUserText(obj_id, "21_LENGTH"))
    width = float(rs.GetUserText(obj_id, "22_WIDTH"))
    height = float(rs.GetUserText(obj_id, "23_HEIGHT"))
    if rs.GetUserText(obj_id, "06_TEMPLATE_DE") == "V-AL09":
        i_no = "1795-4000000004"
        desc = "BL 20mm EN AW-5754H14"
        unit = "m^2"
        quantity = length * width * 1e-06
    elif rs.GetUserText(obj_id, "06_TEMPLATE_DE") == "V-AL35":
        i_no = "2002010013"
        desc = "Alu-Vierkantstab 20mm EN 755-4 EN AW-6060 T66"
        unit = "m"
        quantity = length * 1e-03
    elif rs.GetUserText(obj_id, "06_TEMPLATE_DE") == "V-VA09":
        i_no = "1100571015"
        desc = "BL 15mm 1.4571-S235 1D EN 10088-4"
        unit = "m^2"
        quantity = length * width * 1e-06
    else:
        i_no = ""
        desc = ""
        unit = ""
        quantity = 0

    part = create_part(
        u_no=0,
        s_no=0,
        i_no=i_no,
        desc=desc,
        desc2=create_desc2(part_name) + "-Zuschnitt",
        quantity=quantity,
        unit=unit,
        length=length,
        width=width,
        height=height,
        d_no=part_name + "-01",
        efal=["X", None, None, "X"],
        child_parts={}
    )
    return part


def extract_holoplot_data(obj_ids, holo_num):
    holoplot_parts = create_part(u_no=0,
                                 s_no=0,
                                 i_no="V-AL21",
                                 desc="AL-Element",
                                 desc2="holoplot-{:02d}".format(holo_num),
                                 quantity=1,
                                 unit="Stuck",
                                 length=0,
                                 width=0,
                                 height=0,
                                 d_no="1421-H{:02d}".format(holo_num),
                                 efal=[None, "X", "X", None],
                                 child_parts={}
                                 )
    holoplot_tree = {
        "1421-H{:02d}".format(holo_num): holoplot_parts
    }
    for obj_id in obj_ids:
        part_name1 = get_specific_part_name(obj_id)
        if rs.IsBlockInstance(obj_id):
            if "1421" in part_name1:
                truss = init_part(obj_id)
                truss_part_ids = rs.BlockObjects(rs.BlockInstanceName(obj_id))
                for truss_part_id in truss_part_ids:
                    part_name2 = get_specific_part_name(truss_part_id)
                    if "1421" in part_name2:
                        truss_part = init_part(truss_part_id, obj_id)
                        truss_raw_part = init_raw_part(truss_part_id)
                        truss_part["child_parts"].update({part_name2 + "-Zuschnitt": truss_raw_part})
                        truss["child_parts"].update({part_name2: truss_part})
                holoplot_tree["1421-H{:02d}".format(holo_num)]["child_parts"].update({part_name1: truss})
        elif rs.IsPolysurface(obj_id):
            if "1421" in part_name1:
                part = init_part(obj_id)
                raw_part = init_raw_part(obj_id)
                part["child_parts"].update({part_name1 + "-Zuschnitt": raw_part})
                holoplot_tree["1421-H{:02d}".format(holo_num)]["child_parts"].update({part_name1: part})
    return holoplot_tree


def sort_child_parts(holo_dict):
    for k, v in holo_dict.items():
        if isinstance(v, dict):
            if k != "child_parts":
                v["child_parts"] = OrderedDict(sorted(v["child_parts"].items()))
            sort_child_parts(v)


def set_unique_num(holo_dict):
    global ID_COUNT
    for k, v in holo_dict.items():
        if isinstance(v, dict):
            if k != "child_parts":
                v["u_no"] = ID_COUNT
                ID_COUNT += 1
            set_unique_num(v)


def set_structure_num(holo_dict):
    for k, v in holo_dict.items():
        if isinstance(v, dict):
            if k != "child_parts":
                for k2 in v["child_parts"].keys():
                    v["child_parts"][k2]["s_no"] = v["u_no"]
            set_structure_num(v)


def main():
    holo_num = rs.GetInteger("Holoplot Number")
    sel_obj_ids = rs.GetObjects("Select parts")
    holo_tree_dict = extract_holoplot_data(sel_obj_ids, holo_num)
    sort_child_parts(holo_tree_dict)
    set_unique_num(holo_tree_dict)
    set_structure_num(holo_tree_dict)
    with open("H:\\Desktop\\projects\\holoplot\\H{holo_num:02d}\\H{holo_num:02d}.json".format(holo_num=holo_num), "w") \
            as fp:
        json.dump(holo_tree_dict, fp)


if __name__ == "__main__":
    main()
