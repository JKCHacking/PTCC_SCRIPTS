import argparse
from src.pdf_script import PdfScript
from src.excel_script import ExcelScript


def main(input_pdf_fp, output_xlsx_fp):
    comm_pattern_ls = [
        "AFE;",
        "YKK:",
        "AED:",
        "GENERAL NOTE:",
        "REVERT",
        "REJECTED",
        "TYPE-01",
        "no back panel.",
        "?",
        "DESIGN",
        "confirm"
    ]
    title_pattern = "SD-"
    col_list = ["PTCC", "AED", "YKK", "AFE"]

    ps = PdfScript(input_pdf_fp)
    es = ExcelScript(output_xlsx_fp)
    for page in ps.get_page_from_file():
        page_title = ps.search_title(page, title_pattern)
        worksheet = es.create_worksheet(page_title)
        # setup worksheet
        es.setup_worksheet(worksheet, col_list)
        for content in ps.search_annotations_from_page(page):
            print(" ")

        for found_comments in ps.search_strings_from_page(page, comm_pattern_ls):
            print(" ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("-i", "--input", help="Input PDF file path", type=str)
    parser.add_argument("-o", "--output", help="Output Excel file path", type=str)
    args = parser.parse_args()

    if args.input.endswith(".pdf") and args.output.endswith(".xlsx"):
        main(args.input, args.output)
    else:
        print("Wrong extension files [requirement: .pdf or xlsx]")
