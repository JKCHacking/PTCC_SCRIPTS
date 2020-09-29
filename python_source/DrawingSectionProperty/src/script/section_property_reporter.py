import os
from reportlab.lib.units import inch
from src.util.constants import Constants
from src.fea.pre_processor import PreProcessor
from src.fea.analysis_calculator import AnalysisCalculator
from src.fea.post_processor import PostProcessor


class SectionPropertyReporter:
    def __init__(self, args):
        self.materials = args.m
        self.title = args.t
        self.title_font_size = args.tfs
        self.num_format = args.nf
        self.num_decimal = args.nd
        self.seg_size = args.ms
        self.mesh_size = args.ss
        self.paper_margin = 0.50 * inch
        self.paper_size = args.ps
        self.report_font_size = args.rfs
        self.landscape = args.landscape
        self.long = args.long
        self.weighted = args.weighted
        self.hole = args.hole

    def iter_input(self):
        input_dir = Constants.INPUT_DIR
        mat_list = None
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DXF_FILE_EXT):
                    # Pre-Processor
                    pre_proc = PreProcessor()
                    geometry = pre_proc.create_geometry(file_full_path, self.hole, self.seg_size)
                    mesh = pre_proc.create_mesh(geometry, self.mesh_size)

                    if self.materials:
                        mat_list = pre_proc.create_materials(self.materials)

                    cross_section = pre_proc.create_cross_section(geometry, mesh, mat_list)
                    # Solver
                    cross_section = AnalysisCalculator.calculate_section_properties(cross_section)
                    # Post-Processor
                    post_proc = PostProcessor(geometry,
                                              cross_section,
                                              mat_list,
                                              file_name,
                                              self.title,
                                              self.title_font_size,
                                              self.num_format,
                                              self.num_decimal,
                                              self.paper_size,
                                              self.report_font_size,
                                              self.landscape,
                                              self.weighted,
                                              self.long)
                    post_proc.generate_pdf_report()
