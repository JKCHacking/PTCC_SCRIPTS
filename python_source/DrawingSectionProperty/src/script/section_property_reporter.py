import os
from reportlab.lib.units import inch
from src.util.constants import Constants
from src.fea.pre_processor import PreProcessor


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
        for dir_path, dir_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(Constants.DXF_FILE_EXT):
                    # Pre-Processor
                    # Solver
                    # Post-Processor
                    pass
