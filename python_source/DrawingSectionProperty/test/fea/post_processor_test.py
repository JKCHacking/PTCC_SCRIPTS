import unittest
from src.fea.post_processor import PostProcessor
import src.sectionproperties.pre.sections as sections
from src.sectionproperties.analysis.cross_section import CrossSection


class PostProcessorTest(unittest.TestCase):

    def test_generate_pdf_report(self):
        filename = "filename_stub.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = False
        long = True

        isection = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        box = sections.Rhs(d=100, b=150, t=6, r_out=15, n_r=8, shift=[-8.5, 203])
        geometry = sections.MergedSection([isection, box])
        mesh = geometry.create_mesh([1.5, 2.0])
        cross_section = CrossSection(geometry, mesh)
        cross_section.calculate_geometric_properties()
        cross_section.calculate_plastic_properties()
        cross_section.calculate_warping_properties()

        post_proc = PostProcessor(geometry,
                                  cross_section,
                                  filename,
                                  title,
                                  title_fs,
                                  num_format,
                                  num_decimal,
                                  paper_size,
                                  report_fontsize,
                                  landscape,
                                  weighted,
                                  long)
        post_proc.generate_pdf_report()
