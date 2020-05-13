from src.drawing_scanner import DrawingScanner
from src.constants import Constants
import os

if __name__ == "__main__":
    input_path = os.path.join(Constants.INPUT_DIR, 'input.dwg')
    output_path = os.path.join(Constants.OUTPUT_DIR, 'output.csv')

    ds = DrawingScanner()
    document = ds.open_file(input_path)
    ms = ds.get_modelspace(document)
    data_dict = ds.search_blocks(ms)

