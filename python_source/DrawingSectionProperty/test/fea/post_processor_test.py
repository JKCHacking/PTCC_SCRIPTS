import unittest
from src.fea.post_processor import PostProcessor
import src.sectionproperties.pre.sections as sections
from src.sectionproperties.analysis.cross_section import CrossSection
from src.sectionproperties.pre.pre import Material


class PostProcessorTest(unittest.TestCase):

    def test_generate_long_report(self):
        """
        No Material
        """

        # Typical Settings
        filename = "long_0_mat.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        materials = []

        # Test
        long = True
        weighted = False

        geometry = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        mesh = geometry.create_mesh([1.5])
        cross_section = CrossSection(geometry, mesh)
        cross_section.calculate_geometric_properties()
        cross_section.calculate_plastic_properties()
        cross_section.calculate_warping_properties()

        post_proc = PostProcessor(geometry,
                                  cross_section,
                                  materials,
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

    def test_generate_short_report(self):
        """
        No Material
        """
        filename = "short_0_mat.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = False
        long = False
        materials = []

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
                                  materials,
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

    def test_generate_long_report_1_mat(self):
        """
        1 Material
        """
        filename = "long_1_mat.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = False
        long = True

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )

        materials = [timber]

        geometry = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        mesh = geometry.create_mesh([1.5])
        cross_section = CrossSection(geometry, mesh)
        cross_section.calculate_geometric_properties()
        cross_section.calculate_plastic_properties()
        cross_section.calculate_warping_properties()

        post_proc = PostProcessor(geometry,
                                  cross_section,
                                  materials,
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

    def test_generate_short_report_1_mat(self):
        """
        1 Material
        """
        filename = "short_1_mat.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = False
        long = False

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )
        materials = [timber]

        geometry = sections.ISection(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
        mesh = geometry.create_mesh([1.5])
        cross_section = CrossSection(geometry, mesh)
        cross_section.calculate_geometric_properties()
        cross_section.calculate_plastic_properties()
        cross_section.calculate_warping_properties()

        post_proc = PostProcessor(geometry,
                                  cross_section,
                                  materials,
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

    def test_generate_long_report_2_mat(self):
        """
        2 Material
        """
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

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )

        concrete = Material(
            name='Concrete', elastic_modulus=30.1e3, poissons_ratio=0.2, yield_strength=32,
            color='lightgrey'
        )

        materials = [timber, concrete]

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
                                  materials,
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

    def test_generate_short_report_2_mat(self):
        """
        2 Material
        """
        filename = "filename_stub.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = False
        long = False

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )

        concrete = Material(
            name='Concrete', elastic_modulus=30.1e3, poissons_ratio=0.2, yield_strength=32,
            color='lightgrey'
        )

        materials = [timber, concrete]

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
                                  materials,
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

    def test_generate_long_report_2_mat_weighted(self):
        """
        2 Material
        """
        filename = "filename_stub.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = True
        long = True

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )

        concrete = Material(
            name='Concrete', elastic_modulus=30.1e3, poissons_ratio=0.2, yield_strength=32,
            color='lightgrey'
        )

        materials = [timber, concrete]

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
                                  materials,
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

    def test_generate_short_report_2_mat_weighted(self):
        """
        2 Material
        """
        filename = "filename_stub.pdf"
        title = "Cross Sectional Properties Report"
        title_fs = 16
        num_format = "float"
        num_decimal = 2
        paper_size = "A4"
        report_fontsize = 10
        landscape = False
        weighted = True
        long = False

        timber = Material(
            name='Timber', elastic_modulus=8e3, poissons_ratio=0.35, yield_strength=20,
            color='burlywood'
        )

        concrete = Material(
            name='Concrete', elastic_modulus=30.1e3, poissons_ratio=0.2, yield_strength=32,
            color='lightgrey'
        )

        materials = [timber, concrete]

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
                                  materials,
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
