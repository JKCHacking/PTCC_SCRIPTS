from reportlab.lib.units import inch


class PostProcessor:
    def __init__(self, cross_section):
        self.cross_sec = cross_section

    def process_centroid_output(self):
        pass

    def process_fea_mesh_output(self):
        pass

    def process_xsec_geom_output(self):
        pass

    def process_xsecprop_report(self):
        pass

    def add_header(self):
        pass

    def add_footer(self):
        pass

    def create_pdf(self,
                   filename,
                   title,
                   title_fontsize,
                   num_format,
                   num_decimal,
                   paper_size,
                   report_fontsize,
                   landscape,
                   weighted,
                   long):

        paper_margin = 0.50 * inch
        if long:
            # add cross section geometry
            # finite element mesh
            pass
        # centroids
        # cross sectional properties report
        pass


