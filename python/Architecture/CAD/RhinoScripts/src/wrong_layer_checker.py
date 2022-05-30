import rhinoscriptsyntax as rs

def check_layer_names(objects):
    wrong_layers = []
    for obj in objects:
        part_name = get_part_name(obj)
        if rs.IsBlockInstance(obj):
            # check the truss first
            if isWrong(obj) and part_name not in wrong_layers:
                wrong_layers.append(part_name)
            # then check all its parts
            parts = rs.BlockObjects(rs.BlockInstanceName(obj))
            for part in parts:
                part_part_name = get_part_name(part)
                if isWrong(part) and part_part_name not in wrong_layers:
                    wrong_layers.append(part_part_name)
        else:
            if isWrong(obj) and part_name not in wrong_layers:
                wrong_layers.append(part_name)
    return wrong_layers


def get_part_name(obj):
    return rs.ObjectLayer(obj).split("::")[-1]


def isWrong(obj):
    wrong = False
    part_name = get_part_name(obj)
    if part_name.startswith("1421") and "..." not in part_name:
        wrong = True
    return wrong


def main():
    objects = rs.AllObjects()
    wrong_layers = check_layer_names(objects)
    print("Wrong Part Names:\n{}".format("\n".join(wrong_layers)))


if __name__ == "__main__":
    main()