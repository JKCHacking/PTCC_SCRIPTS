import os
from src.views_extractor import ViewsExtractor
from src.constants import Constants


def main():
    view_list = ["top", "front", "top_left"]
    views_ext = ViewsExtractor(Constants.OUTPUT_DIR, view_list)
    for dir_path, dir_names, file_names in os.walk(Constants.INPUT_DIR):
        for file_name in file_names:
            if file_name.endswith(".ipt") or file_name.endswith(".iam"):
                model_path = os.path.join(dir_path, file_name)
                views_ext.extract_views(model_path)


if __name__ == "__main__":
    main()
