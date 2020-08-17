import argparse
import os
from src.script.dwg_edu_fixer import main
from src.application.cad_app import CadApp
from src.application.trueview_app import TrueViewerApp


if __name__ == "__main__":
    cad_app = CadApp()
    cad_app.start_app()

    tv_app = TrueViewerApp()
    tv_app.start_app()

    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("--input", help="Input DWG File or Folder", type=str)
    parser.add_argument("--txt", help="File that contains list of files to check", type=str)
    args = parser.parse_args()

    if args.input and os.path.exists(args.input):
        main(args.input, cad_app, tv_app)
    elif args.txt and os.path.exists(args.txt):
        main(args.txt, cad_app, tv_app)
    else:
        print("Invalid input, please check your input commands.")

    tv_app.exit_app()
    cad_app.exit_app()
