import argparse
import os
from src.script.drawing_table_extractor_v2 import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="main")
    parser.add_argument("--input", help="Input DWG File or Folder", type=str)
    args = parser.parse_args()

    if args.input and os.path.exists(args.input):
        main(args.input)
    else:
        print("Invalid input, please check your input commands.")
