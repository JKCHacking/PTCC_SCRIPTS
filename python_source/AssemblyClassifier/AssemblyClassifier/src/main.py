import os
from assembly_classifier import AssemblyClassifier
from constants import Constants


def main():
    asm_classifier = AssemblyClassifier(Constants.OUTPUT_DIR)
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".iam"):
                print("[MAIN]Working with file {}".format(file_name))
                asm_full_path = os.path.join(dir_path, file_name)
                asm_classifier.collect_parts(asm_full_path)


if __name__ == "__main__":
    main()
