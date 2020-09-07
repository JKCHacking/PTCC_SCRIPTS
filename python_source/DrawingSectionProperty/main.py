import argparse
from src.script.section_property_reporter import SectionPropertyReporter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Computes section properties of cross sections from .dxf file/s'
                                                 'of given material/s (-m).')
    parser.add_argument('-m',
                        metavar='MatName',
                        type=str,
                        choices=['aluminum_ams_nmms',
                                 'aluminum_bs_nmms',
                                 'carbon_steel_ams_nmms',
                                 'carbon_steel_bs_nmms',
                                 'stainless_steel_ams_nmms',
                                 'stainless_steel_bs_nmms'],
                        nargs='*',
                        help='material name/s; built-in materials are: '
                             'aluminum_ams_nmms, '
                             'aluminum_bs_nmms, '
                             'carbon_steel_ams_nmms, '
                             'carbon_steel_bs_nmms, '
                             'stainless_steel_ams_nmms, '
                             'stainless_steel_bs_nmms '
                             '(note: materials other than mentioned can be defined per instance)')

    parser.add_argument('-t',
                        metavar='ReportTitle',
                        type=str,
                        default="Cross-Sectional Properties Report",
                        help='title of report output (default: "Cross-Sectional Properties Report"')

    parser.add_argument('-tfs',
                        metavar='TitleFontSize',
                        type=float,
                        default=16,
                        help='report title font size, in pt. (default: 16')

    parser.add_argument('-nf',
                        metavar='NumFormat',
                        type=str,
                        choices=['float', 'exponential'],
                        default='float',
                        help="number format (default is float)")

    parser.add_argument('-nd',
                        metavar='NumDecimal',
                        type=int,
                        default=2,
                        help='number of decimal places (default = 2)')

    parser.add_argument('-ms',
                        metavar='MeshSize',
                        type=float,
                        default=5.0,
                        help='mesh size, percent wrt to minimum shape size (default = 5 [5/100])')

    parser.add_argument('-ss',
                        metavar='SegSize',
                        type=float,
                        default=0.25,
                        help='curve segment size, percent wrt to minimum shape size (default = 0.25 [0.25/100])')

    parser.add_argument('-ps',
                        metavar='PaperSize',
                        type=str,
                        choices=['A4', 'A3', 'LETTER', 'LEGAL'],
                        default='A4',
                        help="output paper size ('A4' [default], 'A3', 'LETTER', 'LEGAL')")

    parser.add_argument('-rfs',
                        metavar='ReportFontSize',
                        type=float,
                        default=10,
                        help="output report font size, in pt. (default: 10)")

    parser.add_argument('-landscape',
                        action="store_true",
                        help='select to print output in landscape mode')

    parser.add_argument('-long',
                        action="store_true",
                        help='outputs long form report')

    parser.add_argument('-weighted',
                        action="store_true",
                        help='outputs report with modulus-weighted values (if material/s is/are specified)')

    parser.add_argument('-hole',
                        action="store_true",
                        help='select to check and add hole reference points')

    args = parser.parse_args()
    script = SectionPropertyReporter(args)
    script.iter_input()
