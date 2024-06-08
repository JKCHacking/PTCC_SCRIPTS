import os
import sys
import tkinter
from pathlib import Path
from views_extractor import ViewsExtractor
from tkinter.filedialog import askopenfilenames

SRC_DIR = ""
if getattr(sys, "frozen", False):
    SRC_DIR = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    SRC_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(SRC_DIR, "output")

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)


def main():
    tkinter.Tk().withdraw()
    inventor_files = askopenfilenames(title="Select the inventor files to convert",
                                      filetypes=[("Inventor Files", ".ipt .iam")])
    views_ext = ViewsExtractor(OUTPUT_DIR)
    for inv_file in inventor_files:
        inv_file_path = Path(inv_file)
        file_name = inv_file_path.name
        abs_file_path = str(inv_file_path.absolute())
        print("[MAIN] Working with file {}".format(file_name))
        dwg_path = views_ext.extract_2d_views(abs_file_path)
        if dwg_path:
            views_ext.fix_inventor_dwg(dwg_path)
            print("[MAIN] saved DWG file {} in {}".format(os.path.basename(dwg_path), OUTPUT_DIR))
            # delete bak files
            os.remove("{}.bak".format(os.path.splitext(dwg_path)[0]))


if __name__ == "__main__":
    main()
