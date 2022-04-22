import array
from comtypes import client

BIN_GAP = 10


class Obj:
    def __init__(self, doc, position, width, length):
        self.doc = doc
        self.position = position
        self.width = width
        self.length = length
        self.obj = None

    def create(self):
        model_space = self.doc.ModelSpace
        ll = [self.position[0], self.position[1], self.position[2]]
        lr = [self.position[0] + self.width, self.position[1], self.position[2]]
        ur = [self.position[0] + self.width, self.position[1] + self.length, self.position[2]]
        ul = [self.position[0], self.position[1] + self.length, self.position[2]]
        # create the vertices using the four corners of the box
        vertices = [ll[0], ll[1], ll[2],
                    lr[0], lr[1], lr[2],
                    ur[0], ur[1], ur[2],
                    ul[0], ul[1], ul[2],
                    ll[0], ll[1], ll[2]]
        self.obj = model_space.AddPolyline(array.array("d", vertices))


class Item(Obj):
    def __init__(self, doc, position, width, length):
        super().__init__(doc, position, width, length)
        self.create()


class Bin(Obj):
    def __init__(self, doc, position, width, length):
        super().__init__(doc, position, width, length)
        self.levels = [[0, 0, 0]]
        self.items = []
        self.create()

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
        for i, level in enumerate(self.levels):
            ent.Move(array.array("d", item.position), array.array("d", level))
            # we should also consider the level lines
            is_fit = self.is_fit(item)
            if is_fit:  # item fits in the given location.
                # add the item to the bin's item list
                self.items.append(item)
                # should add new level and move the start position of the current level.
                min_pt, max_pt = ent.GetBoundingBox()
                self.levels.append([min_pt[0], max_pt[1], 0.0])
                self.levels[i] = [max_pt[0], level[1], 0.0]
                # sort the levels according to top-bottom left-right.
                self.levels = sorted(self.levels, key=lambda k: [k[1], k[0]])
                res = True
                break
            else:
                ent.Move(array.array("d", level), array.array("d", item.position))
        return res


def get_app():
    bs_app = client.GetActiveObject("BricscadApp.AcadApplication")
    return bs_app


def main():
    pass


if __name__ == "__main__":
    main()
