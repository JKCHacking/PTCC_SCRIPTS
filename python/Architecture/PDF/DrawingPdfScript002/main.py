import argparse
from src.pdf_script import PdfScript
from src.excel_script import ExcelScript


def main(input_pdf_fp, output_xlsx_fp):
    comm_pattern_ls = [
        "AFE;",
        "YKK:",
        "AED:",
        "GENERAL NOTE:",
        "CANOPY RAFTER & PURLIN",
        "GRADE SS 316",
        "REVERT TO ORIGINAL DESIGN",
        "OTHERWISE DWG TO BE REJECTED",
        "no back panel",
        "DESIGN CHANGE BY YKK",
        "CONFIRMED BY DESIGN",
        "PLEASE REMOVE OFF SD",
        "fritting pattern",
        "call out 1:20",
        "Railing height",
        "COORDINATE KERB",
        "DIM?",
        "BALCONIES UPDATED",
        "indicate and show",
        "SETTINGOUT BMU PENDING",
        "PATTERN TO BE",
        "IS THIS",
        "ADD REFERENCE",
        "PLAN OF SS RAILING",
        "ELEVATION OF SS RAILING",
        "REFERENCE SECTION",
        "REFLECTED SOFFIT",
        "REFLECTED PLAN",
        "ENLARGE 1:20",
        "PROVIDE INTERNAL",
        "DIM TO NEXT GLASS",
        "FAP SILL",
        "CLEAR OPENING",
        "YKK SHOULD BE AWARE",
        "IS NOT GOING TO",
        "TO APPLY TO ALL DOOR TYPES",
        "CLEAR DOOR OPENING",
        "??!!",
        "SAME COMMENTS AS",
        "SHOW MULLION",
        "SHOW 3D",
        "ALSO SHOW",
        "JOINTS?",
        "CALL OUT",
        "REFER",
        "WHERE IS",
        "THIS IS",
        "@1ST",
        "FOR WHAT?",
        "WATERPROOFING",
        "FORTIS TO",
        "ALL BRACKET SYSTEM",
        "ALL MEP PENETRATION",
        "ALL GLASS FOR",
        "BMU SYSTEM",
        "PENETRATION AT ALUM"
    ]

    title_pattern = "SD-"
    col_list = ["PTCC", "AED", "YKK", "AFE", "OTHERS"]

    ps = PdfScript(input_pdf_fp)
    es = ExcelScript(output_xlsx_fp)

    for pagenum, page in enumerate(ps.get_page_from_file()):
        print(f"Current Page Number: {pagenum}")
        page_title = ps.search_title(page, title_pattern)
        worksheet = es.create_worksheet(page_title)

        # setup worksheet for every page
        es.setup_worksheet(worksheet, col_list)
        ptcc_col = 1

        for content in ps.search_annotations_from_page(page):
            row = es.get_nrows_in_col(worksheet, ptcc_col) + 1
            pos = (row, ptcc_col)
            es.add_worksheet_contents(worksheet, content, pos)

        for row, res_tup in enumerate(ps.search_strings_from_page(page, comm_pattern_ls)):
            comment = res_tup[0]
            commenter = res_tup[1]

            if commenter == "AED:":
                col = 2
            elif commenter == "YKK:":
                col = 3
            elif commenter == "AFE;":
                col = 4
            else:
                col = 5  # default to OTHERS column

            row = es.get_nrows_in_col(worksheet, col) + 1
            pos = (row, col)
            es.add_worksheet_contents(worksheet, comment, pos)

    es.save_workbook()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("-i", "--input", help="Input PDF file path", type=str)
    parser.add_argument("-o", "--output", help="Output Excel file path", type=str)
    args = parser.parse_args()

    if args.input.endswith(".pdf") and args.output.endswith(".xlsx"):
        main(args.input, args.output)
    else:
        print("Wrong file extension [requirement: .pdf as input and .xlsx as output]")
