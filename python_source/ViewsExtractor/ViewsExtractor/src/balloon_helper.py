import math
import array
import ctypes
from comtypes import automation


class BalloonHelper:
    def __init__(self, inv_app):
        self.inv_app = inv_app
        self.top_line = None
        self.btm_line = None
        self.left_line = None
        self.right_line = None
        self.view_margin = 2
        self.vertical_offset = 0.9
        self.horizontal_offset = 1

    def add_balloon_to_view(self, view):
        part_list = view.Parent.PartsLists.Item(1)
        # self.__initialise_view_bounding_box(view)
        for row in part_list.PartsListRows:
            # if not row.Ballooned:
            self.__create_row_item_balloon(row, view)
        self.__arrange_balloons_on_view(view)

    # def __initialise_view_bounding_box(self, view):
    #     trans_geom = self.inv_app.TransientGeometry
    #     top_left = trans_geom.CreatePoint2d(view.Left, view.Top)
    #     top_right = trans_geom.CreatePoint2d(view.Left + view.Width, view.Top)
    #     btm_left = trans_geom.CreatePoint2d(view.Left, view.Top - view.Height)
    #     btm_right = trans_geom.CreatePoint2d(view.Left + view.Width, view.Top - view.Height)
    #
    #     self.top_line = trans_geom.CreateLineSegment2d(top_left, top_right)
    #     self.btm_line = trans_geom.CreateLineSegment2d(btm_left, btm_right)
    #     self.left_line = trans_geom.CreateLineSegment2d(top_left, btm_left)
    #     self.right_line = trans_geom.CreateLineSegment2d(top_right, btm_right)

    def __create_row_item_balloon(self, row, view):
        trans_geom = self.inv_app.TransientGeometry
        attach_point = self.__get_balloon_attach_geom(row, view)
        if attach_point is not None:
            balloon_position = self.__get_balloon_position(attach_point.PointOnSheet, view)
            leader_points = self.inv_app.TransientObjects.CreateObjectCollection()
            leader_points.Add(balloon_position)
            leader_points.Add(attach_point)
            view.Parent.Balloons.Add(leader_points)

    def __arrange_balloons_on_view(self, view):
        left_balloons = []
        right_balloons = []
        top_balloons = []
        btm_balloons = []

        for balloon in view.Parent.Balloons:
            if balloon.ParentView is view:
                if balloon.Position.X == view.Left - self.view_margin:
                    left_balloons.append(balloon)
                elif balloon.Position.X == view.Left + view.Width + self.view_margin:
                    right_balloons.append(balloon)
                elif balloon.Position.Y == view.Top + self.view_margin:
                    top_balloons.append(balloon)
                elif balloon.Position.Y == view.Top - view.Height - self.view_margin:
                    btm_balloons.append(balloon)
        if len(left_balloons) > 1:
            self.__arrange_balloon_vertically(left_balloons)
        if len(right_balloons) > 1:
            self.__arrange_balloon_vertically(right_balloons)
        if len(top_balloons) > 1:
            self.__arrange_balloon_horizontally(top_balloons)
        if len(btm_balloons) > 1:
            self.__arrange_balloon_horizontally(btm_balloons)

    def __arrange_balloon_vertically(self, balloons):
        pass

    def __arrange_balloon_horizontally(self, balloons):
        pass

    def __get_balloon_position(self, attach_point, view):
        leader_point = attach_point
        quadrant = self.__get_quadrant(attach_point, view)
        if quadrant == "Top":
            leader_point.Y = view.Top + self.view_margin
            translation_ratio = (leader_point.Y - view.Center.Y) / (attach_point.Y - view.Center.Y)
            leader_point.X = view.Center.X + (attach_point.X - view.Center.X) * translation_ratio
        elif quadrant == "Bottom":
            leader_point.Y = view.Top - view.Height - self.view_margin
            translation_ratio = (leader_point.Y - view.Center.Y) / (attach_point.Y - view.Center.Y)
            leader_point.X = view.Center.X + (attach_point.X - view.Center.X) * translation_ratio
        elif quadrant == "Left":
            leader_point.X = view.Left - self.view_margin
            translation_ratio = (leader_point.X - view.Center.X) / (attach_point.X - view.Center.X)
            leader_point.Y = view.Center.Y + (attach_point.Y - view.Center.Y) * translation_ratio
        elif quadrant == "Right":
            leader_point.X = view.Left - self.view_margin
            translation_ratio = (leader_point.X - view.Center.X) / (attach_point.X - view.Center.X)
            leader_point.Y = view.Center.Y + (attach_point.Y - view.Center.Y) * translation_ratio
        else:
            print("Quadrant not found")
            return None
        return leader_point

    def __get_quadrant(self, attach_point, view):
        corner_angle = math.atan2(view.Height, view.Width)
        point_angle = math.atan2(attach_point.Y - view.Center.Y, attach_point.X - view.Center.X)
        quadrant = None
        if corner_angle > point_angle > -corner_angle:
            quadrant = "Right"
        if corner_angle < point_angle < math.pi - corner_angle:
            quadrant = "Top"
        if point_angle > math.pi - corner_angle or point_angle < -math.pi + corner_angle:
            quadrant = "Left"
        if -math.pi + corner_angle < point_angle < -corner_angle:
            quadrant = "Bottom"
        return quadrant

    def __get_balloon_attach_geom(self, row, view):
        row_occurrences_enumerator = view.ReferencedDocumentDescriptor.ReferencedDocument.ComponentDefinition\
            .Occurrences.AllReferencedOccurrences(row.ReferencedFiles.Item(1).DocumentDescriptor)
        curves = self.__get_curves_from_occ(row_occurrences_enumerator, view)
        # get the first segment
        segment = curves[0].Segments.Item(1)
        return self.__get_attach_point(segment)

    def __get_attach_point(self, segment):
        attach_point = None
        if segment is not None:
            drawing_sheet = segment.Parent.Parent.Parent
            # case when the segment is a line
            attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, self.__get_segment_midpoint(segment))
            # case when the segment is circular
            # kCircleCurve2d = 5252, kEllipseFullCurve2d = 5254
            if segment.GeometryType == 5252 or segment.GeometryType == 5254:
                quadrant = self.__get_quadrant(segment.Geometry.Center, segment.Parent.Parent)
                if quadrant == "Top":
                    k_circular_top_point_intent = 57863
                    attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, k_circular_top_point_intent)
                elif quadrant == "Bottom":
                    k_circular_bottom_point_intent = 57864
                    attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, k_circular_bottom_point_intent)
                elif quadrant == "Left":
                    k_circular_left_point_intent = 57861
                    attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, k_circular_left_point_intent)
                elif quadrant == "Right":
                    k_circular_right_point_intent = 57862
                    attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, k_circular_right_point_intent)
                else:
                    k_center_point_intent = 57860
                    attach_point = drawing_sheet.CreateGeometryIntent(segment.Parent, k_center_point_intent)
        return attach_point

    def __get_curves_from_occ(self, occs_enum, view):
        curves = []
        for occurrence in occs_enum:
            if not occurrence.Suppressed:
                for curve in view.DrawingCurves(occurrence):
                    if curve not in curves:
                        curves.append(curve)
        return curves

    def __get_segment_midpoint(self, segment):
        double_array_2 = ctypes.c_double * 2
        double_array_1 = ctypes.c_double * 1
        curve_eval = segment.Geometry.Evaluator
        min_param = ctypes.c_double()
        max_param = ctypes.c_double()
        mid_param = ctypes.c_double()
        curve_len = ctypes.c_double()
        mid_param_arr = automation.VARIANT(array.array("d", [0]))
        mid_point_coordinate = automation.VARIANT(array.array("d", [0, 0]))

        curve_eval.GetParamExtents(ctypes.byref(min_param), ctypes.byref(max_param))
        curve_eval.GetLengthAtParam(min_param, max_param, ctypes.byref(curve_len))
        curve_eval.GetParamAtLength(min_param, curve_len.value / 2, ctypes.byref(mid_param))
        # we need to use other variable to hold the mid param value since GetParamAtLength requires
        # to be a non-array variable but GetPointAtParam requires an array variable.
        # mid_param_arr[0] = mid_param.value
        curve_eval.GetPointAtParam(ctypes.byref(mid_param_arr), ctypes.byref(mid_point_coordinate))
        return self.inv_app.TransientGeometry.CreatePoint2d(mid_point_coordinate[0], mid_point_coordinate[1])

    # def __get_best_segment_from_occ(self, curves):
    #     best_rating = 0
    #     best_segment = None
    #     for curve in curves:
    #         rating = 0
    #         best_in_curve, rating = self.__get_best_segment_from_curve(curve, rating)
    #         if rating > best_rating:
    #             best_segment = best_in_curve
    #             best_rating = rating
    #     return best_segment
    #
    # def __get_best_segment_from_curve(self, curve, rating):
    #     best_segment = None
    #     segment_rating = 0
    #     for segment in curve.Segments:
    #         seg_len = self.__get_segment_length(segment)
    #         seg_points = self.__split_segment(segment, 10)
    #         closest_dist = math.inf
    #         distance_sum = 0
    #         for point in seg_points:
    #             point_dist = self.__distance_to_view_rangebox(point, curve.Parent)
    #             if point_dist < closest_dist:
    #                 closest_dist = point_dist
    #             distance_sum += point_dist
    #         avg_dist = distance_sum / len(seg_points)
    #         rating = seg_len
    #         k_tangent_edge = 82694
    #         if curve.EdgeType == k_tangent_edge:
    #             rating /= 10
    #         if rating > segment_rating:
    #             best_segment = segment
    #             segment_rating = rating
    #     return best_segment, segment_rating
    #
    # def __split_segment(self, segment, split_precision):
    #     point_list = []
    #     min_param = automation.VARIANT(array.array("d", [0]))
    #     max_param = automation.VARIANT(array.array("d", [0]))
    #     ref_min_param = byref(min_param)
    #     ref_max_param = byref(max_param)
    #
    #     trans_geom = self.inv_app.TransientGeometry
    #     segment.Geometry.Evaluator.GetParamExtents(ref_min_param, ref_max_param)
    #     min_param = ref_min_param
    #     max_param = ref_max_param
    #     for i in range(split_precision):
