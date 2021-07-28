import os
import argparse
from views_extractor import ViewsExtractor
from constants import Constants


def iter_input(views_ext):
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".ipt"):
                print("[MAIN] Working with file {}".format(file_name))
                model_path = os.path.join(dir_path, file_name)
                dwg_path = views_ext.extract_2d_views(model_path)
                if dwg_path:
                    views_ext.fix_inventor_dwg(dwg_path)
                    print("[MAIN] saved DWG file {} in {}".format(os.path.basename(dwg_path), Constants.OUTPUT_DIR))
                    # delete bak files
                    os.remove("{}.bak".format(os.path.splitext(dwg_path)[0]))


def main():
    views_ext = ViewsExtractor(Constants.OUTPUT_DIR)
    iter_input(views_ext)


if __name__ == "__main__":
    main()
