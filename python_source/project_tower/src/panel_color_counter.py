from comtypes import client
import array


def main():
    bricscad_app = client.GetActiveObject("BricscadApp.AcadApplication", dynamic=True)
    bricscad_app.Visible = True

    doc = bricscad_app.ActiveDocument
    ss_obj = doc.SelectionSets.Add("test")

    point1 = array.array("d", [0, 0, 0])
    point2 = array.array("d", [0, 0, 0])

    point1 = doc.Utility.GetPoint(point1, "Specify first corner: ")
    point2 = doc.Utility.GetPoint(point2, "Specify opposite corner: ")

    color_dict = {
        "red": [255, 0, 0],
        "orange": [255, 165, 0],
        "yellow": [255, 255, 0],
        "yellow_green": [60, 80, 20],
        "green": [0, 128, 0],
        "blue": [0, 0, 255],
        "violet": [238, 130, 238]
    }
    red_count = 0
    orange_count = 0
    yellow_count = 0
    yellow_green_count = 0
    green_count = 0
    blue_count = 0
    violet_count = 0

    ss_obj.Select(0, array.array("d", list(point1)), array.array("d", list(point2)))
    for obj in ss_obj:
        ac_color = obj.TrueColor
        rgb = []
        rgb.append(ac_color.Red)
        rgb.append(ac_color.Green)
        rgb.append(ac_color.Blue)
        for key, value in color_dict.items():
            if value == rgb:
                if key == "red":
                    red_count += 1
                elif key == "orange":
                    orange_count += 1
                elif key == "yellow":
                    yellow_count += 1
                elif key == "yellow_green":
                    yellow_green_count += 1
                elif key == "green":
                    green_count += 1
                elif key == "blue":
                    blue_count += 1
                elif key == "violet":
                    violet_count += 1
    ss_obj.Delete()
    print("{},{},{},{},{},{},{}".format(
        red_count,
        orange_count,
        yellow_count,
        yellow_green_count,
        green_count,
        blue_count,
        violet_count
    ))


if __name__ == "__main__":
    main()

