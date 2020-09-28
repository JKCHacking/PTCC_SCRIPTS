import os
import fitz
from math import floor
from reportlab.lib.units import inch
from src.util.constants import Constants


class PostProcessor:
    def __init__(self,
                 geometry,
                 cross_section,
                 material_list,
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
        self.cross_sec = cross_section
        self.geometry = geometry
        self.materials = material_list
        self.filename = filename
        self.title = title
        self.title_fontsize = title_fontsize
        self.num_format = num_format
        self.num_decimal = num_decimal
        self.paper_size = paper_size
        self.report_fontsize = report_fontsize
        self.landscape = landscape
        self.weighted = weighted
        self.long = long
        self.paper_margin = 0.50 * inch

    def __put_figure_in_page(self, fig, axis, pdf_doc, ps_rect, figure_output_fp):
        # axis.legend(loc="upper right", bbox_to_anchor=(1, 1))
        fig.set_figwidth(Constants.FIGURE_WIDTH)
        fig.set_figheight(Constants.FIGURE_HEIGHT)
        fig.savefig(figure_output_fp, dpi=300)

        page = pdf_doc.newPage(width=ps_rect.width, height=ps_rect.height)
        # add the header
        self.__add_header(page)
        # add the footer
        self.__add_footer(page)
        # add the image
        figure_f = open(figure_output_fp, "rb")
        figure_stream = figure_f.read()
        figure_rect = fitz.Rect(self.paper_margin,
                                self.paper_margin + Constants.IMAGE_HEIGHT,
                                page.rect.width - self.paper_margin,
                                page.rect.height - self.paper_margin - Constants.IMAGE_HEIGHT)
        page.insertImage(figure_rect, stream=figure_stream, keep_proportion=False)
        figure_f.close()
        os.remove(figure_output_fp)
        return pdf_doc

    def __add_centroid_page(self, pdf_doc, paper_size_rect):
        temp_centroid_fp = os.path.join(Constants.OUTPUT_DIR, "centroid.jpg")
        fig, ax = self.cross_sec.plot_centroids(pause=False)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_centroid_fp)

    def __add_mesh_page(self, pdf_doc, paper_size_rect):
        temp_mesh_fp = os.path.join(Constants.OUTPUT_DIR, "mesh.jpg")
        fig, ax = self.cross_sec.plot_mesh(pause=False, materials=True)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_mesh_fp)

    def __add_geom_page(self, pdf_doc, paper_size_rect):
        temp_geom_fp = os.path.join(Constants.OUTPUT_DIR, "geom.jpg")
        fig, ax = self.geometry.plot_geometry(pause=False)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_geom_fp)

    def __add_report_page(self, pdf_doc, paper_size_rect):
        num_form = f"{{:.{self.num_decimal}f}}"
        if self.num_format == "Exponential":
            num_form = f"{{:.{self.num_decimal}e}}"
        report_content = ""
        page = pdf_doc.newPage(width=paper_size_rect.width, height=paper_size_rect.height)

        # add the header
        self.__add_header(page)
        # add the footer
        self.__add_footer(page)

        report_content += "\nSection Properties:\n\n"

        if self.materials:
            if len(self.materials) == 1:
                report_content += "Material Elastic Modulus                               E  =  " +\
                                  f"{self.materials[0].elastic_modulus}\n"
                report_content += "Material Yield Strength                               Fy  =  " +\
                                  f"{self.materials[0].yield_strength}\n"
            else:
                for i, mat in enumerate(self.materials):
                    report_content += f"Material {i+1}\n"
                    report_content += "     Material Elastic Modulus                          E  =  " + \
                                      f"{mat.elastic_modulus}\n"
                    report_content += "     Material Yield Strength                          Fy  =  " + \
                                      f"{mat.yield_strength}\n"
            if self.weighted:
                report_content += f"Modulus-weighted Area                                E.A  =  " +\
                                  f"{self.cross_sec.get_ea()}\n"

        if self.long:
            # case where s
            sf_11_plus = self.cross_sec.get_sf_p()[0]
            sf_11_minus = self.cross_sec.get_sf_p()[1]
            sf_22_plus = self.cross_sec.get_sf_p()[2]
            sf_22_minus = self.cross_sec.get_sf_p()[3]

            sf_11_plus = sf_11_plus if sf_11_plus is not None else 0
            sf_11_minus = sf_11_minus if sf_11_minus is not None else 0
            sf_22_plus = sf_22_plus if sf_22_plus is not None else 0
            sf_22_minus = sf_22_minus if sf_22_minus is not None else 0

            long_templ_fp = os.path.join(Constants.TEMPL_DIR, "long_report.txt")
            with open(long_templ_fp, "r") as f:
                templ_contents = f.read()
                templ_contents = templ_contents.format(
                    a=num_form.format(self.cross_sec.get_area()),
                    qx=num_form.format(self.cross_sec.get_q()[0]),
                    qy=num_form.format(self.cross_sec.get_q()[1]),
                    cx=num_form.format(self.cross_sec.get_c()[0]),
                    cy=num_form.format(self.cross_sec.get_c()[1]),
                    ixx_g=num_form.format(self.cross_sec.get_ig()[0]),
                    iyy_g=num_form.format(self.cross_sec.get_ig()[1]),
                    ixy_g=num_form.format(self.cross_sec.get_ig()[2]),
                    ixx_c=num_form.format(self.cross_sec.get_ic()[0]),
                    iyy_c=num_form.format(self.cross_sec.get_ic()[1]),
                    ixy_c=num_form.format(self.cross_sec.get_ic()[2]),
                    cy_plus=None,
                    cy_minus=None,
                    cx_plus=None,
                    cx_minus=None,
                    sxx_plus=None,
                    sxx_minus=None,
                    syy_plus=None,
                    syy_minus=None,
                    rx=num_form.format(self.cross_sec.get_rc()[0]),
                    ry=num_form.format(self.cross_sec.get_rc()[1]),
                    phi=num_form.format(self.cross_sec.get_phi()),
                    i11_c=num_form.format(self.cross_sec.get_ip()[0]),
                    i22_c=num_form.format(self.cross_sec.get_ip()[1]),
                    c2_plus=None,
                    c2_minus=None,
                    c1_plus=None,
                    c1_minus=None,
                    s11_plus=None,
                    s11_minus=None,
                    s22_plus=None,
                    s22_minus=None,
                    r11=num_form.format(self.cross_sec.get_rp()[0]),
                    r22=num_form.format(self.cross_sec.get_rp()[1]),
                    j=num_form.format(self.cross_sec.get_j()),
                    cw=num_form.format(self.cross_sec.get_gamma()),
                    x_se=num_form.format(self.cross_sec.get_sc()[0]),
                    y_se=num_form.format(self.cross_sec.get_sc()[1]),
                    x_st=num_form.format(self.cross_sec.get_sc_t()[0]),
                    y_st=num_form.format(self.cross_sec.get_sc_t()[1]),
                    x_se_o=None,
                    y_se_o=None,
                    x_st_o=None,
                    y_st_o=None,
                    x1_se=num_form.format(self.cross_sec.get_sc_p()[0]),
                    y2_se=num_form.format(self.cross_sec.get_sc_p()[1]),
                    x1_se_o=None,
                    y2_se_o=None,
                    a_sx=num_form.format(self.cross_sec.get_As()[0]),
                    a_sy=num_form.format(self.cross_sec.get_As()[1]),
                    a_s11=num_form.format(self.cross_sec.get_As_p()[0]),
                    a_s22=num_form.format(self.cross_sec.get_As_p()[0]),
                    beta_x_plus=num_form.format(self.cross_sec.get_beta()[0]),
                    beta_x_minus=num_form.format(self.cross_sec.get_beta()[1]),
                    beta_y_plus=num_form.format(self.cross_sec.get_beta()[2]),
                    beta_y_minus=num_form.format(self.cross_sec.get_beta()[3]),
                    beta_11_plus=num_form.format(self.cross_sec.get_beta_p()[0]),
                    beta_11_minus=num_form.format(self.cross_sec.get_beta_p()[1]),
                    beta_22_plus=num_form.format(self.cross_sec.get_beta_p()[2]),
                    beta_22_minus=num_form.format(self.cross_sec.get_beta_p()[3]),
                    x_pc=num_form.format(self.cross_sec.get_pc()[0]),
                    y_pc=num_form.format(self.cross_sec.get_pc()[1]),
                    zxx=None,
                    zyy=None,
                    x11_pc=num_form.format(self.cross_sec.get_pc_p()[0]),
                    y22_pc=num_form.format(self.cross_sec.get_pc_p()[1]),
                    z11=None,
                    z22=None,
                    sf_11_plus=num_form.format(sf_11_plus),
                    sf_11_minus=num_form.format(sf_11_minus),
                    sf_22_plus=num_form.format(sf_22_plus),
                    sf_22_minus=num_form.format(sf_22_minus),
                )

        else:
            short_templ_fp = os.path.join(Constants.TEMPL_DIR, "short_report.txt")
            with open(short_templ_fp, "r") as f:
                templ_contents = f.read()
                templ_contents = templ_contents.format(
                    a=num_form.format(self.cross_sec.get_area()),
                    ixx_c=num_form.format(self.cross_sec.get_ic()[0]),
                    iyy_c=num_form.format(self.cross_sec.get_ic()[1]),
                    ixy_c=num_form.format(self.cross_sec.get_ic()[2]),
                    cy_plus=None,
                    cy_minus=None,
                    cx_plus=None,
                    cx_minus=None,
                    sxx_plus=None,
                    sxx_minus=None,
                    syy_plus=None,
                    syy_minus=None,
                    rx=num_form.format(self.cross_sec.get_rc()[0]),
                    ry=num_form.format(self.cross_sec.get_rc()[1]),
                    phi=num_form.format(self.cross_sec.get_phi()),
                    j=num_form.format(self.cross_sec.get_j()),
                    cw=num_form.format(self.cross_sec.get_gamma()),
                    x_se=num_form.format(self.cross_sec.get_sc()[0]),
                    y_se=num_form.format(self.cross_sec.get_sc()[1]),
                    beta_x_plus=num_form.format(self.cross_sec.get_beta()[0]),
                    beta_x_minus=num_form.format(self.cross_sec.get_beta()[1]),
                    beta_y_plus=num_form.format(self.cross_sec.get_beta()[2]),
                    beta_y_minus=num_form.format(self.cross_sec.get_beta()[3]),
                    x_pc=num_form.format(self.cross_sec.get_pc()[0]),
                    y_pc=num_form.format(self.cross_sec.get_pc()[1]),
                    zxx=None,
                    zyy=None
                )
        report_content += templ_contents
        body_rect = fitz.Rect(self.paper_margin,
                              self.paper_margin + Constants.IMAGE_HEIGHT,
                              page.rect.width - self.paper_margin,
                              page.rect.height - self.paper_margin - Constants.IMAGE_HEIGHT)

        rc = page.insertTextbox(body_rect,
                                report_content,
                                fontsize=self.report_fontsize,
                                expandtabs=8,
                                align=fitz.TEXT_ALIGN_LEFT)
        if rc < 0:  # this is the case when the contents does not fit inside the body space of the page.
            # we have to split the whole content into multiple pages
            # determine the number of lines that can be fit inside
            fit_px = page.insertTextbox(body_rect, '', fontsize=self.report_fontsize)
            # convert to pts
            fit_pts = abs(fit_px * 12 / 16)
            # number of line that will fit inside the box depending on the font size
            fit_lines = floor(fit_pts / self.report_fontsize)
            # getting each line of the content string
            content_lines = report_content.split("\n")
            # total number of lines in the content
            tot_lines = len(content_lines)
            # number of pages that will be used to split the whole contents
            # warning: there will be instance of empty page
            num_pages_res = round(tot_lines / fit_lines)

            start = 0
            end = fit_lines
            for i in range(0, num_pages_res):
                try:
                    if i == 0:  # reuse the previously created page
                        partitioned_content = "\n".join(content_lines[start:end])
                        rc = page.insertTextbox(body_rect,
                                                partitioned_content,
                                                fontsize=self.report_fontsize,
                                                align=fitz.TEXT_ALIGN_JUSTIFY,
                                                expandtabs=8)
                    else:
                        # create a new page
                        page = pdf_doc.newPage(width=paper_size_rect.width, height=paper_size_rect.height)
                        # add the header
                        self.__add_header(page)
                        # add the footer
                        self.__add_footer(page)
                        # add the body parts
                        partitioned_content = "\n".join(content_lines[start:end])
                        rc = page.insertTextbox(body_rect,
                                                "\n" + partitioned_content,
                                                fontsize=self.report_fontsize,
                                                align=fitz.TEXT_ALIGN_JUSTIFY,
                                                expandtabs=8)
                except IndexError as ie:
                    print(str(ie))
                start += fit_lines
                end += fit_lines

        return pdf_doc

    def __add_header(self, p):
        sec_prop_logo_fp = os.path.join(Constants.IMAGES_DIR, 'secprop_logo.jpg')
        logo_f = open(sec_prop_logo_fp, "rb")
        logo_stream = logo_f.read()
        title_point = fitz.Point(self.paper_margin, self.paper_margin + 45)

        logo_rect = fitz.Rect(p.rect.width - self.paper_margin - Constants.IMAGE_WIDTH,
                              self.paper_margin,
                              p.rect.width - self.paper_margin,
                              self.paper_margin + Constants.IMAGE_HEIGHT)

        p.insertText(title_point, self.title, fontsize=self.title_fontsize)
        p.insertImage(logo_rect, stream=logo_stream)
        logo_f.close()

    def __add_footer(self, p):
        sec_prop_lic_fp = os.path.join(Constants.IMAGES_DIR, 'secprop_lic.jpg')
        ptcc_logo_fp = os.path.join(Constants.IMAGES_DIR, 'ptcc_logo.jpg')

        lic_f = open(sec_prop_lic_fp, "rb")
        lic_stream = lic_f.read()
        ptcc_logo_f = open(ptcc_logo_fp, "rb")
        ptcc_logo_stream = ptcc_logo_f.read()

        ptcc_logo_rect = fitz.Rect(self.paper_margin,
                                   p.rect.height - self.paper_margin - Constants.IMAGE_HEIGHT,
                                   self.paper_margin + Constants.IMAGE_WIDTH,
                                   p.rect.height - self.paper_margin)
        p.insertImage(ptcc_logo_rect, stream=ptcc_logo_stream)

        xsec_lic_rect = fitz.Rect(p.rect.width - self.paper_margin - Constants.IMAGE_WIDTH,
                                  p.rect.height - self.paper_margin - Constants.IMAGE_HEIGHT,
                                  p.rect.width - self.paper_margin,
                                  p.rect.height - self.paper_margin)
        p.insertImage(xsec_lic_rect, stream=lic_stream)

        lic_f.close()
        ptcc_logo_f.close()

    def generate_pdf_report(self):
        # determine the paper size
        output_pdf_fp = os.path.join(Constants.OUTPUT_DIR, self.filename)
        if self.paper_size == "A4" and not self.landscape:
            ps_rect = fitz.PaperRect('a4')
        elif self.paper_size == "A4" and self.landscape:
            ps_rect = fitz.PaperRect('a4-l')
        elif self.paper_size == "A3" and not self.landscape:
            ps_rect = fitz.PaperRect('a3')
        elif self.paper_size == "A3" and self.landscape:
            ps_rect = fitz.PaperRect('a3-l')
        elif self.paper_size == "LETTER" and not self.landscape:
            ps_rect = fitz.PaperRect('letter')
        elif self.paper_size == "LETTER" and self.landscape:
            ps_rect = fitz.PaperRect('letter-l')
        elif self.paper_size == "LEGAL" and not self.landscape:
            ps_rect = fitz.PaperRect('legal')
        elif self.paper_size == "LEGAL" and self.landscape:
            ps_rect = fitz.PaperRect('legal-l')

        pdf_doc = fitz.open()
        if self.long:
            # add geometry page
            pdf_doc = self.__add_geom_page(pdf_doc, ps_rect)
            # add mesh page
            pdf_doc = self.__add_mesh_page(pdf_doc, ps_rect)
        # add centroids page
        pdf_doc = self.__add_centroid_page(pdf_doc, ps_rect)
        # add cross sectional properties report page
        pdf_doc = self.__add_report_page(pdf_doc, ps_rect)
        pdf_doc.save(output_pdf_fp)
        print("Generate Report Complete. Can be Found in `output` folder")
