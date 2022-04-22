import tkinter
import csv
import array
from comtypes import client
from tkinter.filedialog import askopenfilename

MARGIN_RIGHT = 10
MARGIN_TOP = 20


class Obj:
    def __init__(self, doc, width, length, color):
        self.doc = doc
        self.width = width
        self.length = length
        self.obj = None
        self.color = color

    def display(self, position):
        model_space = self.doc.ModelSpace
        ll = [position[0], position[1], position[2]]
        lr = [position[0] + self.width, position[1], position[2]]
        ur = [position[0] + self.width, position[1] + self.length, position[2]]
        ul = [position[0], position[1] + self.length, position[2]]
        # create the vertices using the four corners of the box
        vertices = [ll[0], ll[1], ll[2],
                    lr[0], lr[1], lr[2],
                    ur[0], ur[1], ur[2],
                    ul[0], ul[1], ul[2],
                    ll[0], ll[1], ll[2]]
        self.obj = model_space.AddPolyline(array.array("d", vertices))
        self.obj.TrueColor = self.color


class Item(Obj):
    def __init__(self, doc, width, length):
        color = doc.Application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color.SetRGB(0, 255, 0)
        super().__init__(doc, width, length, color)


class Bin(Obj):
    def __init__(self, doc, width, length):
        color = doc.Application.GetInterfaceObject("BricscadDb.AcadAcCmColor")
        color.SetRGB(255, 0, 0)
        super().__init__(doc, width, length, color)
        self.levels = []
        self.items = []

    def is_fit(self, item):
        """
        Description
        ===========
        This function checks whether an item fits a specific space inside the bin.
        Parameters
        ==========
        item:Item - Item to check.
        Return
        ======
        fit:Bool - whether the item fits or not.
        """
        overlap_check = []
        fit = False
        # check if it fits inside the bin
        fit_bin = self.is_fit_bin(item.obj)
        # this is the case if the item does not touch any sides of the bin
        if fit_bin == -1:
            fit = -1
        elif fit_bin:
            fit = True
            if self.items:
                for i in self.items:
                    overlap_check.append(self.is_overlap(i.obj, item.obj))
            if self.levels:
                model_space = self.doc.ModelSpace
                min_pt, max_pt = self.obj.GetBoundingBox()
                for lvl in self.levels:
                    # spawn the level line physically
                    lvl_line = model_space.AddLine(array.array("d", lvl),
                                                   array.array("d", [max_pt[0], lvl[1], 0.0]))
                    overlap_check.append(self.is_overlap(lvl_line, item.obj))
                    lvl_line.Delete()
            if any(overlap_check):
                fit = False
        return fit

    def is_fit_bin(self, ent_item):
        """
        Description
        ===========
        Function to check Bin vs Item. check if Item can fit inside the bin.
        Parameters
        ==========
        ent_item:AcDbPolyline - Entity item to be checked against bin.
        Return
        ======
        fit_bin:Bool/-1 - Check whether the item fits in the bin or not.
                          -1 if item is not touching on any sides of the bin.
        """
        intersection_points = self.obj.IntersectWith(ent_item, 0)
        if intersection_points:
            bin_min, bin_max = self.obj.GetBoundingBox()
            ent_min, ent_max = ent_item.GetBoundingBox()
            if ent_min[0] >= bin_min[0] and ent_max[0] <= bin_max[0] and \
                    ent_min[1] >= bin_min[1] and ent_max[1] <= bin_max[1]:
                fit_bin = True
            else:
                fit_bin = False
        else:
            fit_bin = -1
        return fit_bin

    def is_overlap(self, ent1, ent2):
        """
        Description
        ===========
        This function checks if two items overlap with each other
        Parameters
        ==========
        ent1: AcDbPolyline - first entity to check
        ent2: AcDbPolyline - second entity to check
        Return
        ======
        overlap:Bool - whether the two entities overlap or not.
        """
        ent1_min, ent1_max = ent1.GetBoundingBox()
        ent2_min, ent2_max = ent2.GetBoundingBox()
        # check for overlap in the X and Y Projection
        if ent1_max[0] > ent2_min[0] and ent2_max[0] > ent1_min[0] and \
                ent1_max[1] > ent2_min[1] and ent2_max[1] > ent1_min[1]:
            overlap = True
        else:
            overlap = False
        return overlap

    def add_item(self, item):
        res = False
        ent = item.obj
        old_ent_min, old_ent_max = ent.GetBoundingBox()
        for i, level in enumerate(self.levels):
            curr_ent_min, curr_ent_max = ent.GetBoundingBox()
            ent.Move(array.array("d", list(curr_ent_min)), array.array("d", level))
            # we should also consider the level lines
            is_fit = self.is_fit(item)
            if is_fit:  # item fits in the given location.
                # add the item to the bin's item list
                self.items.append(item)
                # should add new level and move the start position of the current level.
                new_min_pt, new_max_pt = ent.GetBoundingBox()
                self.levels.append([new_min_pt[0], new_max_pt[1], 0.0])
                self.levels[i] = [new_max_pt[0], level[1], 0.0]
                # sort the levels according to top-bottom left-right.
                self.levels = sorted(self.levels, key=lambda k: [k[1], k[0]])
                res = True
                break
        if not res:
            new_ent_min, new_ent_max = ent.GetBoundingBox()
            ent.Move(array.array("d", list(new_ent_min)), array.array("d", list(old_ent_min)))
        return res


def get_app():
    bs_app = client.GetActiveObject("BricscadApp.AcadApplication")
    return bs_app


def main():
    cad = get_app()
    doc = cad.ActiveDocument
    tkinter.Tk().withdraw()
    csv_file_name = askopenfilename(title="Select input CSV file", filetypes=[("CSV Files", ".csv")])
    assemblies = []
    parts = []
    curr_assembly_pos = [0, 0, 0]
    curr_part_pos = [0, 0, 0]
    with open(csv_file_name, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            length = int(row["length"])
            width = int(row["width"])
            if row["designation"] == "assembly":
                assembly = Bin(doc, width, length)
                assemblies.append(assembly)
            else:  # part
                count = int(row["count"])
                for _ in range(count):
                    part = Item(doc, width, length)
                    parts.append(part)
    # sort items according to length (Highest to lowest)
    parts = sorted(parts, key=lambda l: [l.length], reverse=True)
    # display the parts and the initial assembly
    curr_part_pos[1] += assemblies[0].length + MARGIN_TOP
    for p in parts:
        p.display(curr_part_pos)
        curr_part_pos[0] += p.width + MARGIN_RIGHT
    assemblies[0].display(curr_assembly_pos)
    assemblies[0].levels.append(list(assemblies[0].obj.GetBoundingBox()[0]))
    curr_assembly_pos[0] += assemblies[0].width + MARGIN_RIGHT

    for p in parts:
        for i, assm in enumerate(assemblies):
            res = assm.add_item(p)
            if not res and i == len(assemblies) - 1:
                new_assm = Bin(doc, assm.width, assm.length)
                new_assm.display(curr_assembly_pos)
                new_assm.levels.append(list(new_assm.obj.GetBoundingBox()[0]))
                assemblies.append(new_assm)
                curr_assembly_pos[0] += new_assm.width + MARGIN_RIGHT
            elif res:
                break


if __name__ == "__main__":
    main()
