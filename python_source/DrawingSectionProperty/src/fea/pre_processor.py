import numpy as np
import sectionproperties.pre.sections as sections
from src.util.line import get_points_from_line
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.cross_section import CrossSection
from math import ceil
from ezdxf import readfile
from ezdxf import math
from src.util.constants import Constants


class PreProcessor:
    def __init__(self):
        self.geometry_list = []

    def __get_child_entities_within(self, parent_polyline, modelspace):
        ent_child_list = []
        parent_handle = parent_polyline.dxf.handle
        parent_points = parent_polyline.get_points('xy')
        parent_points = self.__convert_to_vec2s(parent_points)

        for ent in modelspace:
            count = 0
            handle = ent.dxf.handle
            entity_type = ent.dxftype()
            points = []

            if parent_handle == handle:
                continue
            if entity_type == "LWPOLYLINE":
                points = ent.get_points('xy')
            elif entity_type == "CIRCLE":
                cent_x, cent_y = ent.dxf.center[:-1]
                radius = ent.dxf.radius
                points = [(cent_x + radius, cent_y), (cent_x, cent_y + radius), (cent_x - radius, cent_y),
                          (cent_x, cent_y - radius)]

            if points:
                points = self.__convert_to_vec2s(points)
                for point in points:
                    if math.is_point_in_polygon_2d(point, parent_points) == 1:
                        count += 1
                    else:
                        break
                if count == len(points):
                    ent_child_list.append(ent)
        return ent_child_list

    def __get_polylines(self, modelspace):
        pl_list = []
        for ent in modelspace:
            if ent.dxftype() == "LWPOLYLINE" or ent.dxftype == "POLYLINE":
                pl_list.append(ent)
        return pl_list

    def __get_points_and_facets(self, parent_pl, child_ent_list, segment_size):
        profile_points = []
        profile_facets = []

        parent_bbox = math.BoundingBox2d(parent_pl.get_points('xy'))
        bbox_x, bbox_y = parent_bbox.size
        shape_size = min(bbox_x, bbox_y)
        seg_size_mult = segment_size / 100
        arc_seg_size = seg_size_mult * shape_size

        for ent in parent_pl.virtual_entities():
            self.__add_to_lists(ent, profile_points, profile_facets, arc_seg_size)
        if child_ent_list:
            for child_ent in child_ent_list:
                if child_ent.dxftype() == "LWPOLYLINE":
                    for ent in child_ent.virtual_entities():
                        self.__add_to_lists(ent, profile_points, profile_facets, arc_seg_size)
                elif child_ent.dxftype() == "CIRCLE":
                    self.__add_to_lists(child_ent, profile_points, profile_facets, arc_seg_size)
        return profile_points, profile_facets

    def __add_to_lists(self, ent, profile_points, profile_facets, arc_seg_size):
        if ent.dxftype() == "LINE":
            start_point = list(ent.dxf.start[:-1])
            end_point = list(ent.dxf.end[:-1])

            s_point = [round(start_point[0], Constants.ROUND_PRECISION),
                       round(start_point[1], Constants.ROUND_PRECISION)]
            e_point = [round(end_point[0], Constants.ROUND_PRECISION),
                       round(end_point[1], Constants.ROUND_PRECISION)]

            if s_point in profile_points and e_point not in profile_points:
                profile_points.append(e_point)
                profile_facets.append([profile_points.index(s_point), len(profile_points) - 1])
            elif e_point in profile_points and s_point not in profile_points:
                profile_points.append(s_point)
                profile_facets.append([profile_points.index(e_point), len(profile_points) - 1])
            elif s_point in profile_points and e_point in profile_points:
                profile_facets.append([profile_points.index(s_point), profile_points.index(e_point)])
            else:
                profile_points.append(s_point)
                profile_points.append(e_point)
                profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])
        elif ent.dxftype() == "CIRCLE" or ent.dxftype() == "ARC":
            seg_arc_points = self.__arc_2_points(ent, arc_seg_size)
            try:
                for ind, _ in enumerate(seg_arc_points):
                    start_point = seg_arc_points[ind]
                    end_point = seg_arc_points[ind + 1]

                    s_point = [round(start_point[0], Constants.ROUND_PRECISION),
                               round(start_point[1], Constants.ROUND_PRECISION)]
                    e_point = [round(end_point[0], Constants.ROUND_PRECISION),
                               round(end_point[1], Constants.ROUND_PRECISION)]

                    if s_point in profile_points and e_point not in profile_points:
                        profile_points.append(e_point)
                        profile_facets.append([profile_points.index(s_point), len(profile_points) - 1])
                    elif e_point in profile_points and s_point not in profile_points:
                        profile_points.append(s_point)
                        profile_facets.append([profile_points.index(e_point), len(profile_points) - 1])
                    elif s_point in profile_points and e_point in profile_points:
                        profile_facets.append([profile_points.index(s_point), profile_points.index(e_point)])
                    else:
                        profile_points.append(s_point)
                        profile_points.append(e_point)
                        profile_facets.append([len(profile_points) - 2, len(profile_points) - 1])
            except IndexError:
                pass

    def __arc_2_points(self, circular_ent, arc_seg_size):
        seg_arc_pts = []

        if circular_ent.dxftype() == "ARC":
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point

            radius = circular_ent.dxf.radius
            s_ang = circular_ent.dxf.start_angle
            e_ang = circular_ent.dxf.end_angle

            if e_ang < s_ang:
                e_ang += 360
        else:  # CIRCLE
            center_point = circular_ent.dxf.center[:-1]
            center_point_x, center_point_y = center_point
            radius = circular_ent.dxf.radius
            s_ang = 0
            e_ang = 360

        tot_ang = e_ang - s_ang
        arc_len = abs(radius * np.radians(tot_ang))
        arc_div = ceil(arc_len / arc_seg_size)

        s_ang_rad = np.radians(s_ang)
        e_ang_rad = np.radians(e_ang)
        arc_T = np.linspace(s_ang_rad, e_ang_rad, arc_div)
        list_x = center_point_x + radius * np.cos(arc_T)
        list_y = center_point_y + radius * np.sin(arc_T)

        for x, y in zip(list_x, list_y):
            seg_arc_pts.append([x, y])
        return seg_arc_pts

    def __get_holes(self, child_ent_list):
        hole_points = []
        for child_ent in child_ent_list:
            if child_ent.dxftype() == "LWPOLYLINE":
                points = child_ent.get_points()
                bbox = math.BoundingBox2d(points)
                bbox_center_x, bbox_center_y = bbox.center
                hole_points.append([round(bbox_center_x, Constants.ROUND_PRECISION),
                                    round(bbox_center_y, Constants.ROUND_PRECISION)])
            else:  # CIRCLE
                center_x, center_y = child_ent.dxf.center[:-1]
                hole_points.append([round(center_x, Constants.ROUND_PRECISION),
                                    round(center_y, Constants.ROUND_PRECISION)])
        return hole_points

    def __get_control_points(self, parent_pl, child_ent_list):
        control_point = []
        parent_points = self.__convert_to_vec2s(parent_pl.get_points('xy'))
        parent_bbox = math.BoundingBox2d(parent_points)
        min_pt = parent_bbox.extmin
        max_pt = parent_bbox.extmax

        # boundary of the parent polyline
        x_min = min_pt[0]
        y_min = min_pt[1]
        x_max = max_pt[0]
        y_max = max_pt[1]

        cp_found = False
        # get the candidate X,Y
        for y in np.arange(y_min, y_max, 0.05):
            for x in np.arange(x_min, x_max, 0.05):
                pt_list = [round(x, Constants.ROUND_PRECISION), round(y, Constants.ROUND_PRECISION)]
                possible_c_point = math.Vec2(pt_list)
                if child_ent_list:  # if there are holes
                    for child_ent in child_ent_list:
                        if child_ent.dxftype() == "LWPOLYLINE":
                            child_points = self.__convert_to_vec2s(child_ent.get_points('xy'))
                            if math.is_point_in_polygon_2d(possible_c_point, parent_points) == 1:
                                if math.is_point_in_polygon_2d(possible_c_point, child_points) == -1:
                                    control_point.append(pt_list)
                                    cp_found = True
                                    break
                        else:  # CIRCLE
                            bbox_child = math \
                                .ConstructionCircle(math.Vec2(child_ent.dxf.center[:-1]), child_ent.dxf.radius) \
                                .bounding_box
                            if math.is_point_in_polygon_2d(possible_c_point, parent_points) == 1 and \
                                    not bbox_child.inside(possible_c_point):
                                control_point.append(pt_list)
                                cp_found = True
                                break
                else:  # when there are no holes
                    if math.is_point_in_polygon_2d(possible_c_point, parent_points) == 1:
                        control_point.append(pt_list)
                        cp_found = True
                        break
                if cp_found:
                    break
            if cp_found:
                break
        return control_point

    def __convert_to_vec2s(self, pt_list):
        vec2_list = []
        for pt in pt_list:
            vec2_pt = math.Vec2(pt)
            vec2_list.append(vec2_pt)
        return vec2_list

    def create_geometry(self, file_fp, has_holes, segment_size):
        """
            creates the geometry of each profile inside the drawing file
        """
        print("Creating geometry...")
        geometry = None
        drawing_file = readfile(file_fp)
        mod_space = drawing_file.modelspace()
        polylines = self.__get_polylines(mod_space)
        contact_points = []

        for polyline in polylines:
            parent_pl = polyline
            child_ent_list = []
            hole_points = []
            if has_holes:
                # if theres a hole there should always be child entities.
                child_ent_list = self.__get_child_entities_within(parent_pl, mod_space)
                hole_points = self.__get_holes(child_ent_list)

            profile_points, profile_facets = self.__get_points_and_facets(parent_pl, child_ent_list, segment_size)
            control_points = self.__get_control_points(parent_pl, child_ent_list)

            if (has_holes and child_ent_list) or not has_holes:
                geometry = sections.CustomSection(
                    profile_points,
                    profile_facets,
                    hole_points,
                    control_points
                )
                self.geometry_list.append(geometry)

        if len(self.geometry_list) > 1:
            geometry = sections.MergedSection(self.geometry_list)

            # there will be possible holes formed by two or more profiles in contact
            # check if there are contacts made by two or more profiles
            for base_geometry in self.geometry_list:
                base_points = base_geometry.points
                base_vec_points = self.__convert_to_vec2s(base_points)
                for comp_geometry in self.geometry_list:
                    if base_geometry is not comp_geometry:
                        comp_points = comp_geometry.points
                        comp_vec_points = self.__convert_to_vec2s(comp_points)
                        for point in base_points:
                            if point in comp_points and point not in contact_points:
                                contact_points.append(point)
                        sorted_con_points = sorted(contact_points, key=lambda k: [k[0], k[1]])
                        for i, con_point in enumerate(sorted_con_points):
                            try:
                                start = con_point
                                end = sorted_con_points[i + 1]
                                possible_hole_points = get_points_from_line(start, end)
                                for h_point in possible_hole_points:
                                    if math.is_point_in_polygon_2d(math.Vec2(h_point), base_vec_points) == -1 and \
                                            math.is_point_in_polygon_2d(math.Vec2(h_point), comp_vec_points) == -1:
                                        geometry.add_hole(h_point)
                                        break
                            except IndexError:
                                break
        elif self.geometry_list:
            geometry = self.geometry_list[0]

        if geometry:
            print("Cleaning geometry...")
            geometry.clean_geometry(verbose=True)
        return geometry

    def create_mesh(self, geometry, mesh_size):
        print("Creating mesh...")
        mesh_sizes = []
        mesh_size_mult = mesh_size / 100

        # get the mesh size for each geometry
        for geom in self.geometry_list:
            x_min, x_max, y_min, y_max = geom.calculate_extents()
            min_size = min(abs(x_max - x_min), abs(y_max - y_min))
            mesh_sizes.append(min_size * mesh_size_mult)

        mesh = geometry.create_mesh(mesh_sizes)
        return mesh

    def create_section(self, geometry, mesh, material_list):
        """
            creates the cross section of given geometry and mesh
            :param
            geometry_list - list of Geometry objects
            mesh_size - mesh size user input.
            :return
            cross_section object
        """
        print("Creating CrossSection...")
        cross_section = CrossSection(geometry, mesh, material_list)
        return cross_section

    def create_materials(self, material_list):
        materials = []
        name = ''
        elastic_modulus = 0
        poissons_ratio = 0
        yield_strength = 0
        color = ''
        for mat in material_list:
            if mat == 'aluminum_ams_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per AA ADM 2015. (Yield stress for 6063-T5.)
                """
                name = 'Aluminum'
                elastic_modulus = 70000
                poissons_ratio = 0.33
                yield_strength = 110
                color = 'green'
            elif mat == 'aluminum_bs_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per BS 8118-1.1991. (Yield stress for 6063-T5.)
                """
                name = 'Aluminum'
                elastic_modulus = 70000
                poissons_ratio = 0.33
                yield_strength = 110
                color = 'green'
            elif mat == 'carbon_steel_ams_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per ANSI AISC 360-16. (Yield stress for A36.)
                """
                name = 'Carbon Steel'
                elastic_modulus = 200000
                poissons_ratio = 0.30
                yield_strength = 250
                color = 'grey'
            elif mat == 'carbon_steel_bs_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per BS 5950-1.2000. (Yield stress for S275.)
                """
                name = 'Carbon Steel'
                elastic_modulus = 205000
                poissons_ratio = 0.30
                yield_strength = 275
                color = 'grey'
            elif mat == 'stainless_steel_ams_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per AISC STEEL DESIGN GUIDE 27. 
                    (Yield stress for S30400, S31600)
                """
                name = 'Stainless Steel'
                elastic_modulus = 193000
                poissons_ratio = 0.30
                yield_strength = 205
                color = 'silver'
            elif mat == 'stainless_steel_bs_nmms':
                """
                    Material properties for aluminum (in N-mm-s) as per SCI P291. (Yield stress for 1.4301 [316])
                """
                name = 'Stainless Steel'
                elastic_modulus = 200000
                poissons_ratio = 0.30
                yield_strength = 210
                color = 'silver'
            else:
                print(f"Input `{mat}` not supported.")
            material = Material(name=name, elastic_modulus=elastic_modulus,
                       poissons_ratio=poissons_ratio, yield_strength=yield_strength, color=color)
            materials.append(material)

        num_mat = len(materials)
        num_geom = len(self.geometry_list)

        diff = abs(num_mat - num_geom)

        if num_mat < num_geom:
            for _ in range(diff):
                materials.append(materials[-1])
        elif num_mat > num_geom:
            for _ in range(diff):
                materials.pop()
        return materials
