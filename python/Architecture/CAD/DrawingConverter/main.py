from src.file_fetcher import FileFetcher
from src.constants import Constants
from src.factory import script_factory


def main(extension):
    for file in FileFetcher.fetch(Constants.INPUT_DIR, extension):
        script = script_factory(extension=extension)
        # check traces of student version in the dwg file [OPTIONAL]
        # if file is a student version
        #   do the conversion method
        #       convert dwg to dxf
        #       convert dxf to dwg
        #   save the new dwg file


if __name__ == "__main__":
    extension = ".dwg"
    main(extension)
