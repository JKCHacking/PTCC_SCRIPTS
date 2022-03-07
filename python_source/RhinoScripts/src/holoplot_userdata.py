import os
import statistics
import rhinoscriptsyntax as rs
import datetime

PROJECT_NUMBER = "1421"
UNIT = rs.UnitSystemName(abbreviate=True)
AL_DEN = 2710  # kg/m^3
SS_DEN = 7849.9764  # kg/m^3
DIM_ROUND_PRECISION = 2
W_ROUND_PRECISION = 4
BB_POINTS = []
HOLO_NUM = ""
ERROR_FILE = "H:\\Desktop\\projects\\holoplot\\HOLOPLOTS\\H{holo_num}\\userdata_err_H{holo_num}.txt"


def main():
    global HOLO_NUM
    HOLO_NUM = rs.GetString("Holoplot Number")
    all_obj_ids = rs.GetObjects("Select objects you want to add Userdata")
    # check all the parts before adding userdata.
    check_parts(all_obj_ids)
    # after checking it will create an error file
    if os.path.exists(ERROR_FILE.format(holo_num=HOLO_NUM)):
        print("There's an error in the holoplot. Please check in the error file.")
    else:
        # add userdata
        add_userdata_objs(all_obj_ids)


def check_parts(obj_ids):
    """
    Desc: Function to check for the correctness of the objects recursively:
        * Wrong layernames
        * engraving tags missing or incompatible
        * openpolysurface
    params: obj_ids - list of object ids
    returns: None
    """
    for obj_id in obj_ids:
        part_name = get_specific_part_name(obj_id)
        if part_name.startswith("1421"):
            if rs.IsBlockInstance(obj_id):
                check_layer_name(obj_id)
                check_parts(rs.BlockObjects(rs.BlockInstanceName(obj_id)))
            elif rs.IsPolysurface(obj_id):
                if not rs.IsPolysurfaceClosed(obj_id):
                    log_error("[{}] Open Polysurface detected.".format(part_name))
                check_layer_name(obj_id)
                get_engravings(obj_id, obj_ids)


def check_layer_name(obj_id):
    part_name = get_part_name(obj_id)
    if isWrong(obj_id):
        log_error("[{}] Wrong layer name".format(part_name))


def isWrong(obj):
    wrong = False
    part_name = get_part_name(obj)
    if part_name.startswith("1421") and "..." not in part_name:
        wrong = True
    return wrong


def add_userdata_objs(obj_ids, parent_block=None):
    """
    Desc: Function that adds userdata to a holoplot recursively.
    param: obj_ids - list of object ids
    return: None
    """
    for obj_id in obj_ids:
        part_name = get_specific_part_name(obj_id)
        if part_name.startswith("1421"):
            print("Working with: {}".format(part_name))
            if rs.IsBlockInstance(obj_id):
                # recurse the parts of the assembly and add userdata
                add_userdata_objs(rs.BlockObjects(rs.BlockInstanceName(obj_id)), obj_id)
                # add userdata to assembly
                add_userdata(obj_id)
            elif rs.IsPolysurfaceClosed(obj_id):
                # add userdata to parts
                add_userdata(obj_id, parent_block)


def log_error(message):
    if os.path.exists(ERROR_FILE.format(holo_num=HOLO_NUM)):
        mode = "a"
    else:
        mode = "w"
    with open(ERROR_FILE.format(holo_num=HOLO_NUM), mode=mode) as err_f:
        err_f.write("[{}]: {}\n".format(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"), message))


def add_userdata(obj_id, parent_block=None):
    spec_pname = get_specific_part_name(obj_id)
    position = get_position(spec_pname)
    revision = get_revision()
    article_at = get_article_at(spec_pname)
    surface = get_surface()
    colour = get_colour()
    screw_lock = get_screw_lock()
    profession = get_profession()
    delivery = get_delivery(parent_block)
    group = get_group(obj_id)
    category = get_category(spec_pname)
    material = get_material(group)
    template_at = get_template_at(group, category)
    template_de, template_name_de = get_template(obj_id)
    name = get_name(spec_pname, category)
    length, width, height = get_dimensions(obj_id, parent_block)
    gross_area = get_gross_area(length, width)
    mass = get_weight(obj_id, group)
    coating_area = get_coating_area(obj_id)
    net_area = coating_area

    rs.SetUserText(obj_id, "01_POSITION", position)
    rs.SetUserText(obj_id, "02_REVISION", revision)
    rs.SetUserText(obj_id, "03_ARTICLE_AT", article_at)
    rs.SetUserText(obj_id, "04_TEMPLATE_AT", template_at)
    rs.SetUserText(obj_id, "05_ARTICLE_DE", article_at)
    rs.SetUserText(obj_id, "06_TEMPLATE_DE", template_de)
    rs.SetUserText(obj_id, "07_TEMPLATE_NAME_DE", template_name_de)
    rs.SetUserText(obj_id, "08_RAWMAT_NO_DE", template_de)
    rs.SetUserText(obj_id, "09_RAWMAT_NAME_DE", template_name_de)
    rs.SetUserText(obj_id, "10_NAME", name)
    rs.SetUserText(obj_id, "11_MATERIAL", material)
    rs.SetUserText(obj_id, "12_MASS", str(mass))
    rs.SetUserText(obj_id, "13_SURFACE", surface)
    rs.SetUserText(obj_id, "14_COLOUR", colour)
    rs.SetUserText(obj_id, "15_SCREW_LOCK", screw_lock)
    rs.SetUserText(obj_id, "21_LENGTH", str(length))
    rs.SetUserText(obj_id, "22_WIDTH", str(width))
    rs.SetUserText(obj_id, "23_HEIGHT", str(height))
    rs.SetUserText(obj_id, "31_COATING_AREA", str(coating_area))
    rs.SetUserText(obj_id, "32_GROSS_AREA", str(gross_area))
    rs.SetUserText(obj_id, "33_NET_AREA", str(net_area))
    rs.SetUserText(obj_id, "51_GROUP", group)
    rs.SetUserText(obj_id, "52_PROFESSION", profession)
    rs.SetUserText(obj_id, "53_DELIVERY", delivery)
    rs.SetUserText(obj_id, "54_CATEGORY", category)
    rs.SetUserText(obj_id, "55_ASSEMBLY", HOLO_NUM)
    rs.ObjectName(obj_id, name)


def get_specific_part_name(obj_id):
    layer = rs.ObjectLayer(obj_id)
    spec_pname = layer.split("::")[-1].split("...")[0].strip()
    return spec_pname


def get_part_name(obj):
    return rs.ObjectLayer(obj).split("::")[-1]


def get_position(spec_name):
    position_list = spec_name.split("-")[1:]
    position = "-".join(position_list)
    return position


def get_revision():
    revision = "00"
    return revision


def get_article_at(spec_name):
    article_at = spec_name
    return article_at


def get_template_at(group, category):
    template_at = ""
    if group == "SS sheet":  # stainless steel
        if "Single" in category:
            template_at = "2106"
    else:  # aluminum
        if "Single" in category:
            template_at = "2065"
        elif "Assembly" in category:
            template_at = "2152"
    return template_at


def get_article_de(spec_name):
    article_de = spec_name
    return article_de


def get_template(obj_id):
    template_name_de = ""
    template_de = ""
    layer = rs.ObjectLayer(obj_id)
    base_layer_name = layer.split("::")[-1]
    if "top chord" in base_layer_name or \
        "bottom chord" in base_layer_name or \
        "vertical part" in base_layer_name or \
        "extension part" in base_layer_name or \
        "end part" in base_layer_name:
        template_de = "V-AL09"
        template_name_de = "AL-Blechteil"
    elif "horizontal part" in base_layer_name or \
        "diagonal part" in base_layer_name or \
        "profile" in base_layer_name:
        template_de = "V-AL35"
        template_name_de = "AL-Profilzuschnitt"
    elif "connection part" in base_layer_name:
        template_de = "V-VA09"
        template_name_de = "VA-Blechteil"
    elif "TRUSS" in base_layer_name:
        template_de = "V-AL21"
        template_name_de = "AL-Element"
    return template_de, template_name_de


def get_name(spec_name, category):
    name_dict = {
        "": "",
        "T": "truss assembly",
        "B": "bracing",
        "F": "frame",
        "TC": "top chord",
        "BC": "bottom chord",
        "EX": "extension part",
        "DP": "diagonal part",
        "PR": "profile",
        "CP": "connection part",
        "EP": "end part",
        "VP": "vertical part",
        "HP": "horizontal part",
        "STC": "standard top chord",
        "SBC": "standard bottom chord",
        "SDP": "standard diagonal part",
        "SCP": "standard connection part",
        "SVP": "standard vertical part"
    }
    p_type = ""
    p = ""
    if category == "Pre-Assembly":
        p = spec_name.split("-")[2]
    elif category == "Standard Parts Assembly" or category == "Single Part":
        p = spec_name.split("-")[3]
    elif category == "Standard Parts Single":
        p = spec_name.split("-")[1]

    for c in p:
        if c.isalpha():
            p_type += c
    name = "{} ... {}".format(spec_name, name_dict[p_type])
    return name


def get_material(group):
    material = ""
    if group == "AL sheet":
        material = "aluminum EN AW-5754"
    elif group == "AL profile":
        material = "aluminum EN AW-6060 T66"
    elif group == "SS sheet":
        material = "stainless steel 1.4571"
    return material


def get_weight(obj_id, group):
    tot_sv = 0
    if rs.IsBlockInstance(obj_id):
        orig_blk_name = rs.BlockInstanceName(obj_id)
        part_ids = rs.BlockObjects(orig_blk_name)
        for part_id in part_ids:
            if rs.IsPolysurface(part_id):
                sv = rs.SurfaceVolume(part_id)[0]
                if UNIT == "mm":
                    tot_sv += sv * 1e-09  # convert to meters3
                else:
                    tot_sv += sv
    elif rs.IsPolysurface(obj_id):
        sv = rs.SurfaceVolume(obj_id)[0]
        if UNIT == "mm":
            tot_sv = sv * 1e-09  # convert to meters3
        else:
            tot_sv = sv
    if group == "SS sheet":
        weight = round(tot_sv * SS_DEN, W_ROUND_PRECISION)
    else:
        weight = round(tot_sv * AL_DEN, W_ROUND_PRECISION)
    return weight


def get_surface():
    surface = "anodized E6/C-35"
    return surface


def get_colour():
    colour = "black"
    return colour


def get_screw_lock():
    screw_lock = "NO"
    return screw_lock


def get_dimensions(obj_id, parent_block=None):
    bb_points = []
    length = 0
    width = 0
    height = 0
    ref_engraving_id = None
    if rs.IsBlockInstance(obj_id):
        # get all the truss parts
        blk_name = rs.BlockInstanceName(obj_id)
        truss_part_ids = rs.BlockObjects(blk_name)
        # find the bottom chord engraving text object
        for truss_part_id in truss_part_ids:
            truss_part_name = get_specific_part_name(truss_part_id)
            if "TC" in truss_part_name:
                ref_engraving_id = get_engravings(truss_part_id, truss_part_ids)
                break
        if ref_engraving_id:
            plane = rs.TextObjectPlane(ref_engraving_id)
            bb_points = rs.BoundingBox(truss_part_ids, view_or_plane=plane)
    elif rs.IsPolysurface(obj_id):
        if parent_block:
            blk_name = rs.BlockInstanceName(parent_block)
            blk_objs = rs.BlockObjects(blk_name)
            ref_engraving_id = get_engravings(obj_id, blk_objs)
        else:
            ref_engraving_id = get_engravings(obj_id)

        if ref_engraving_id:
            plane = rs.TextObjectPlane(ref_engraving_id)
            bb_points = rs.BoundingBox(obj_id, view_or_plane=plane)

    if bb_points:
        dim1 = rs.Distance(bb_points[0], bb_points[1])
        dim2 = rs.Distance(bb_points[0], bb_points[4])
        dim3 = rs.Distance(bb_points[1], bb_points[2])
        # im not sure how to label the actual dimension taken from the bounding box.
        # im just going to based on the fact that its dimension is Length > Width > Height.
        dims_list = [dim1, dim2, dim3]
        length = round(max(dims_list), DIM_ROUND_PRECISION)
        width = round(statistics.median(dims_list), DIM_ROUND_PRECISION)
        height = round(min(dims_list), DIM_ROUND_PRECISION)
    return length, width, height


def get_engravings(part_id, all_obj_ids=None):
    position_list = get_specific_part_name(part_id).split("-")[1:]
    position = " ".join(position_list)
    if not all_obj_ids:
        all_obj_ids = rs.AllObjects()

    txt_ids = []
    for obj_id in all_obj_ids:
        if rs.IsText(obj_id) and \
                "".join(rs.TextObjectText(obj_id).split()).lower() == "".join(position.split()).lower():
            txt_ids.append(obj_id)

    if txt_ids:
        part_cent_pt = rs.SurfaceVolumeCentroid(part_id)[0]
        txt_pt_list = [rs.TextObjectPoint(txt_id) for txt_id in txt_ids]
        pt_ids = rs.AddPoints(txt_pt_list)
        closest_pt_id, pt_obj = rs.PointClosestObject(part_cent_pt, pt_ids)
        txt_id = txt_ids[txt_pt_list.index(pt_obj)]
        rs.DeleteObjects(pt_ids)
    else:
        txt_id = None
        log_error("[{}]Cannot find engraving".format(get_specific_part_name(part_id)))
    return txt_id


def get_coating_area(obj_id):
    tot_c_area = 0
    if rs.IsPolysurface(obj_id):
        tot_c_area += rs.SurfaceArea(obj_id)[0]
        if UNIT == "mm":
            tot_c_area = tot_c_area * 1e-06
    elif rs.IsBlockInstance(obj_id):
        orig_blk_name = rs.BlockInstanceName(obj_id)
        part_ids = rs.BlockObjects(orig_blk_name)
        for part_id in part_ids:
            if rs.IsPolysurface(part_id):
                sa = rs.SurfaceArea(part_id)[0]
                if UNIT == "mm":
                    tot_c_area += sa * 1e-06  # convert to meters^2
                else:
                    tot_c_area += sa
    tot_c_area = round(tot_c_area, W_ROUND_PRECISION)
    return tot_c_area


def get_gross_area(length, width):
    gross_area = length * width
    if UNIT == "mm":
        gross_area *= 1e-06  # convert to meters^2
    return round(gross_area, W_ROUND_PRECISION)


def get_group(obj_id):
    layer = rs.ObjectLayer(obj_id)
    group = "AL sheet"
    if "profile" in layer:
        group = "AL profile"
    elif "connection part" in layer:
        group = "SS sheet"
    return group


def get_profession():
    profession = "HOL"
    return profession


def get_delivery(parent_block=None):
    delivery = "S"
    if parent_block:
        delivery = "F"
    return delivery


def get_category(spec_name):
    category = ""
    spec_name_list = spec_name.split("-")
    # not a standard
    if spec_name_list[1].startswith("H"):
        # check if single or assembly
        if len(spec_name_list) == 4:  # single
            if "SP" in spec_name_list[2]:
                category = "Standard Parts Assembly"
            else:
                category = "Single Part"
        elif len(spec_name_list) == 3:  # assembly
            category = "Pre-Assembly"
    elif spec_name_list[1].startswith("S"):  # standard
        category = "Standard Parts Single"
    return category


if __name__ == "__main__":
    main()
