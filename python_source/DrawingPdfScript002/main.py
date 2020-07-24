import argparse
from src.pdf_script import PdfScript
from src.excel_script import ExcelScript


def main(input_pdf_fp, output_xlsx_fp):
    comm_pattern_ls = [
        "AFE;",
        "YKK:",
        "AED:",
    ]
    others_pattern_ls = [
        "GENERAL NOTE:",
        "REVERT",
        "REJECTED",
        "TYPE-01",
        "no back panel.",
        "?",
        "confirm"
    ]
    title_pattern = "SD-"
    col_list = ["PTCC", "AED", "YKK", "AFE", "OTHERS"]

    ps = PdfScript(input_pdf_fp)
    es = ExcelScript(output_xlsx_fp)

    for page in ps.get_page_from_file():
        page_title = ps.search_title(page, title_pattern)
        worksheet = es.create_worksheet(page_title)
        # setup worksheet
        es.setup_worksheet(worksheet, col_list)
        ptcc_col = 1
        for row, content in enumerate(ps.search_annotations_from_page(page)):
            row = row + 1
            pos = (row, ptcc_col)
            es.add_worksheet_contents(worksheet, content, pos, overwrite=False)

        for row, res_tup in enumerate(ps.search_strings_from_page(page, comm_pattern_ls)):
            row = row + 1
            comment = res_tup[0]
            commenter = res_tup[1]

            if "AED" in commenter:
                col = 2
            elif "YKK" in commenter:
                col = 3
            elif "AFE" in commenter:
                col = 4
            else:
                col = 5  # default to OTHERS column
            pos = (row, col)
            es.add_worksheet_contents(worksheet, comment, pos, overwrite=False)

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
