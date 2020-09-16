import os
import fitz
from reportlab.lib.units import inch
from src.util.constants import Constants


class PostProcessor:
    def __init__(self,
                 geometry,
                 cross_section,
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
        axis.legend(loc="upper right", bbox_to_anchor=(1, 1))
        fig.set_figwidth(Constants.FIGURE_WIDTH)
        fig.set_figheight(Constants.FIGURE_HEIGHT)
        fig.savefig(figure_output_fp, dpi=300)

        page = pdf_doc.newPage(width=ps_rect.width, height=ps_rect.height)
        # add the header
        self.__add_header(page)
        # add the footer
        self.__add_footer(page)
        # add the image
        centroid_f = open(figure_output_fp, "rb")
        centroid_stream = centroid_f.read()
        centroid_rect = fitz.Rect(self.paper_margin,
                                  self.paper_margin + Constants.IMAGE_HEIGHT,
                                  page.rect.width - self.paper_margin,
                                  page.rect.height - self.paper_margin - Constants.IMAGE_HEIGHT)
        page.insertImage(centroid_rect, stream=centroid_stream, keep_proportion=False)
        centroid_f.close()
        os.remove(figure_output_fp)
        return pdf_doc

    def __add_centroid_page(self, pdf_doc, paper_size_rect):
        temp_centroid_fp = os.path.join(Constants.OUTPUT_DIR, "centroid.jpg")
        fig, ax = self.cross_sec.plot_centroids(pause=False)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_centroid_fp)

    def __add_mesh_page(self, pdf_doc, paper_size_rect):
        temp_mesh_fp = os.path.join(Constants.OUTPUT_DIR, "mesh.jpg")
        fig, ax = self.cross_sec.plot_mesh(pause=False)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_mesh_fp)

    def __add_geom_page(self, pdf_doc, paper_size_rect):
        temp_geom_fp = os.path.join(Constants.OUTPUT_DIR, "geom.jpg")
        fig, ax = self.geometry.plot_geometry(pause=False)
        return self.__put_figure_in_page(fig, ax, pdf_doc, paper_size_rect, temp_geom_fp)

    def __add_report_page(self, pdf_doc, paper_size_rect):
        page = pdf_doc.newPage(width=paper_size_rect.width, height=paper_size_rect.height)

        # add the header
        self.__add_header(page)
        # add the footer
        self.__add_footer(page)

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


