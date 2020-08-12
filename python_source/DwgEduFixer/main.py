import argparse
import os
from src.script.dwg_edu_fixer import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("--in_file", help="Input DWG File", type=str)
    parser.add_argument('--in_folder', help="Input DWG Folder", type=str)
    args = parser.parse_args()

    if args.in_file and os.path.isfile(args.in_file):
        main(args.in_file)
    elif args.in_folder and os.path.isdir(args.in_folder):
        main(args.in_folder)
    else:
        print("Invalid input, please check your input commands.")
