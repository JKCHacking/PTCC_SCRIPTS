import os
from src.solid_2_assembly import Solid2Assembly
from src.constants import Constants


def iter_input():
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".ipt"):
                yield os.path.join(dir_path, file_name)


def main():
    solid_merger = Solid2Assembly(Constants.OUTPUT_DIR)
    for input_file in iter_input():
        print("[MAIN]Working with file: {}".format(os.path.basename(input_file)))
        solid_merger.merge_to_assembly(input_file)


if __name__ == "__main__":
    main()
