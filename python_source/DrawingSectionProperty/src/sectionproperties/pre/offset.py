import copy
from shapely.geometry.polygon import LinearRing
import matplotlib.pyplot as plt


def offset_perimeter(geometry, offset, side='left', plot_offset=False):
    """Offsets the perimeter of a geometry of a :class:`~sectionproperties.pre.sections.Geometry`
    object by a certain distance. Note that the perimeter facet list must be entered in a
    consecutive order.

    :param geometry: Cross-section geometry object
    :type geometry: :class:`~sectionproperties.pre.sections.Geometry`
    :param float offset: Offset distance for the perimeter
    :param string side: Side of the perimeter offset, either 'left' or 'right'. E.g. 'left' for a
        counter-clockwise offsets the perimeter inwards.
    :param bool plot_offset: If set to True, generates a plot comparing the old and new geometry

    The following example 'corrodes' a 200UB25 I-section by 1.5 mm and compares a few of the
    section properties::

        import sectionproperties.pre.sections as sections
        from sectionproperties.pre.offset import offset_perimeter
        from sectionproperties.analysis.cross_section import CrossSection

        # calculate original section properties
        original_geometry = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=16)
        original_mesh = original_geometry.create_mesh(mesh_sizes=[3.0])
        original_section = CrossSection(original_geometry, original_mesh)
        original_section.calculate_geometric_properties()
        original_area = original_section.get_area()
        (original_ixx, _, _) = original_section.get_ic()

        # calculate corroded section properties
        corroded_geometry = offset_perimeter(original_geometry, 1.5, plot_offset=True)
        corroded_mesh = corroded_geometry.create_mesh(mesh_sizes=[3.0])
        corroded_section = CrossSection(corroded_geometry, corroded_mesh)
        corroded_section.calculate_geometric_properties()
        corroded_area = corroded_section.get_area()
        (corroded_ixx, _, _) = corroded_section.get_ic()

        # compare section properties
        print("Area reduction = {0:.2f}%".format(
            100 * (original_area - corroded_area) / original_area))
        print("Ixx reduction = {0:.2f}%".format(
            100 *(original_ixx - corroded_ixx) / original_ixx))

    The following plot is generated by the above example:

    ..  figure:: ../images/offset_example.png
        :align: center
        :scale: 75 %

        200UB25 with 1.5 mm corrosion.

    The following is printed to the terminal:

    .. code-block:: text

      Area reduction = 41.97%
      Ixx reduction = 39.20%
    """

    # initialise perimeter points list
    perimeter_points = []

    # add perimeter points to the list
    for facet_idx in geometry.perimeter:
        # get the facet
        facet = geometry.facets[facet_idx]

        # get the first point on the facet
        point = geometry.points[facet[0]]

        # add the (x,y) tuple to the list
        perimeter_points.append((point[0], point[1]))

    # create LinearRing object
    perimeter = LinearRing(perimeter_points)

    # offset perimeter
    new_perimeter = perimeter.parallel_offset(
        distance=offset, side=side, resolution=0, join_style=2
    )
    (new_xcoords, new_ycoords) = new_perimeter.xy

    # create deep copy of original geometry object
    new_geometry = copy.deepcopy(geometry)

    # replace offset points in new geometry
    for (i, facet_idx) in enumerate(new_geometry.perimeter):
        # get the facet
        facet = new_geometry.facets[facet_idx]

        # get the first point on the facet
        point = new_geometry.points[facet[0]]

        # replace the point location with the offset location
        point[0] = new_xcoords[i]
        point[1] = new_ycoords[i]

    if plot_offset:
        (fig, ax) = plt.subplots()

        # plot new geometry
        for (i, f) in enumerate(new_geometry.facets):
            if i == 0:
                ax.plot([new_geometry.points[f[0]][0], new_geometry.points[f[1]][0]],
                        [new_geometry.points[f[0]][1], new_geometry.points[f[1]][1]],
                        'ko-', markersize=2, label='Offset Geometry')
            else:
                ax.plot([new_geometry.points[f[0]][0], new_geometry.points[f[1]][0]],
                        [new_geometry.points[f[0]][1], new_geometry.points[f[1]][1]],
                        'ko-', markersize=2)

        # plot the original perimeter
        for (i, facet_idx) in enumerate(geometry.perimeter):
            f = geometry.facets[facet_idx]

            if i == 0:
                ax.plot([geometry.points[f[0]][0], geometry.points[f[1]][0]],
                        [geometry.points[f[0]][1], geometry.points[f[1]][1]],
                        'r--', markersize=2, label='Original Perimeter')
            else:
                ax.plot([geometry.points[f[0]][0], geometry.points[f[1]][0]],
                        [geometry.points[f[0]][1], geometry.points[f[1]][1]],
                        'r--', markersize=2)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_title('Offset Geometry')
        ax.set_aspect('equal', anchor='C')
        plt.tight_layout()
        plt.show()

    return new_geometry
