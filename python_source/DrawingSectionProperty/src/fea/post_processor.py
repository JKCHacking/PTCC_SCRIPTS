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
                report_content += f"Material Elastic Modulus                               E  =  " \
                                  f"{self.materials[0].elastic_modulus}\n"
                report_content += f"Material Yield Strength                               Fy  =  " \
                                  f"{self.materials[0].yield_strength}\n"
            else:
                for i, mat in enumerate(self.materials):
                    report_content += f"Material {i+1}\n"
                    report_content += f"     Material Elastic Modulus                          E  =  " \
                                      f"{mat.elastic_modulus}\n"
                    report_content += f"     Material Yield Strength                          Fy  =  " \
                                      f"{mat.yield_strength}\n"
            if self.weighted:
                report_content += f"Modulus-weighted Area                                E.A  =  " \
                                  f"{self.cross_sec.get_ea()}\n"

        a = self.cross_sec.get_area()
        ixx_c, iyy_c, ixy_c = self.cross_sec.get_ic()
        zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.cross_sec.get_z()
        cy_plus = ixx_c / zxx_plus
        cy_minus = ixx_c / zxx_minus
        cx_plus = iyy_c / zyy_plus
        cx_minus = iyy_c / zyy_minus
        rx, ry = self.cross_sec.get_rc()
        phi = self.cross_sec.get_phi()
        j = self.cross_sec.get_j()
        cw = self.cross_sec.get_gamma()
        x_se, y_se = self.cross_sec.get_sc()
        beta_x_plus, beta_x_minus, beta_y_plus, beta_y_minus = self.cross_sec.get_beta()
        x_pc, y_pc = self.cross_sec.get_pc()
        zxx, zyy = self.cross_sec.get_s()

        if self.long:
            qx, qy = self.cross_sec.get_q()
            cx, cy = self.cross_sec.get_c()
            ixx_g, iyy_g, ixy_g = self.cross_sec.get_ig()
            i11_c, i22_c = self.cross_sec.get_ip()
            z11_plus, z11_minus, z22_plus, z22_minus = self.cross_sec.get_zp()
            r11, r22 = self.cross_sec.get_rp()
            x_st, y_st = self.cross_sec.get_sc_t()
            x1_se, y2_se = self.cross_sec.get_sc_p()
            a_sx, a_sy = self.cross_sec.get_As()
            a_s11, a_s22 = self.cross_sec.get_As_p()
            beta_11_plus, beta_11_minus, beta_22_plus, beta_22_minus = self.cross_sec.get_beta_p()
            z11, z22 = self.cross_sec.get_sp()
            x11_pc, y22_pc = self.cross_sec.get_pc_p()
            c2_plus = i11_c / z11_plus
            c2_minus = i11_c / z11_minus
            c1_plus = i22_c / z22_plus
            c1_minus = i22_c / z22_minus
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
                    a=num_form.format(a),
                    qx=num_form.format(qx),
                    qy=num_form.format(qy),
                    cx=num_form.format(cx),
                    cy=num_form.format(cy),
                    ixx_g=num_form.format(ixx_g),
                    iyy_g=num_form.format(iyy_g),
                    ixy_g=num_form.format(ixy_g),
                    ixx_c=num_form.format(ixx_c),
                    iyy_c=num_form.format(iyy_c),
                    ixy_c=num_form.format(ixy_c),
                    cy_plus=num_form.format(cy_plus),
                    cy_minus=num_form.format(cy_minus),
                    cx_plus=num_form.format(cx_plus),
                    cx_minus=num_form.format(cx_minus),
                    sxx_plus=num_form.format(zxx_plus),
                    sxx_minus=num_form.format(zxx_minus),
                    syy_plus=num_form.format(zyy_plus),
                    syy_minus=num_form.format(zyy_minus),
                    rx=num_form.format(rx),
                    ry=num_form.format(ry),
                    phi=num_form.format(phi),
                    i11_c=num_form.format(i11_c),
                    i22_c=num_form.format(i22_c),
                    c2_plus=num_form.format(c2_plus),
                    c2_minus=num_form.format(c2_minus),
                    c1_plus=num_form.format(c1_plus),
                    c1_minus=num_form.format(c1_minus),
                    s11_plus=num_form.format(z11_plus),
                    s11_minus=num_form.format(z11_minus),
                    s22_plus=num_form.format(z22_plus),
                    s22_minus=num_form.format(z22_minus),
                    r11=num_form.format(r11),
                    r22=num_form.format(r22),
                    j=num_form.format(j),
                    cw=num_form.format(cw),
                    x_se=num_form.format(x_se),
                    y_se=num_form.format(y_se),
                    x_st=num_form.format(x_st),
                    y_st=num_form.format(y_st),
                    # x_se_o=None,
                    # y_se_o=None,
                    # x_st_o=None,
                    # y_st_o=None,
                    x1_se=num_form.format(x1_se),
                    y2_se=num_form.format(y2_se),
                    # x1_se_o=None,
                    # y2_se_o=None,
                    a_sx=num_form.format(a_sx),
                    a_sy=num_form.format(a_sy),
                    a_s11=num_form.format(a_s11),
                    a_s22=num_form.format(a_s22),
                    beta_x_plus=num_form.format(beta_x_plus),
                    beta_x_minus=num_form.format(beta_x_minus),
                    beta_y_plus=num_form.format(beta_y_plus),
                    beta_y_minus=num_form.format(beta_y_minus),
                    beta_11_plus=num_form.format(beta_11_plus),
                    beta_11_minus=num_form.format(beta_11_minus),
                    beta_22_plus=num_form.format(beta_22_plus),
                    beta_22_minus=num_form.format(beta_22_minus),
                    x_pc=num_form.format(x_pc),
                    y_pc=num_form.format(y_pc),
                    zxx=num_form.format(zxx),
                    zyy=num_form.format(zyy),
                    x11_pc=num_form.format(x11_pc),
                    y22_pc=num_form.format(y22_pc),
                    z11=num_form.format(z11),
                    z22=num_form.format(z22),
                    sf_11_plus=num_form.format(sf_11_plus),
                    sf_11_minus=num_form.format(sf_11_minus),
                    sf_22_plus=num_form.format(sf_22_plus),
                    sf_22_minus=num_form.format(sf_22_minus)
                )
        else:
            short_templ_fp = os.path.join(Constants.TEMPL_DIR, "short_report.txt")
            with open(short_templ_fp, "r") as f:
                templ_contents = f.read()
                templ_contents = templ_contents.format(
                    a=num_form.format(a),
                    ixx_c=num_form.format(ixx_c),
                    iyy_c=num_form.format(iyy_c),
                    ixy_c=num_form.format(ixy_c),
                    cy_plus=num_form.format(cy_plus),
                    cy_minus=num_form.format(cy_minus),
                    cx_plus=num_form.format(cx_plus),
                    cx_minus=num_form.format(cx_minus),
                    sxx_plus=num_form.format(zxx_plus),
                    sxx_minus=num_form.format(zxx_minus),
                    syy_plus=num_form.format(zyy_plus),
                    syy_minus=num_form.format(zyy_minus),
                    rx=num_form.format(rx),
                    ry=num_form.format(ry),
                    phi=num_form.format(phi),
                    j=num_form.format(j),
                    cw=num_form.format(cw),
                    x_se=num_form.format(x_se),
                    y_se=num_form.format(y_se),
                    beta_x_plus=num_form.format(beta_x_plus),
                    beta_x_minus=num_form.format(beta_x_minus),
                    beta_y_plus=num_form.format(beta_y_plus),
                    beta_y_minus=num_form.format(beta_y_minus),
                    x_pc=num_form.format(x_pc),
                    y_pc=num_form.format(y_pc),
                    zxx=num_form.format(zxx),
                    zyy=num_form.format(zyy)
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
