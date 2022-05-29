from src.drawing_scanner import DrawingScanner
from src.constants import Constants
import os
import csv

if __name__ == "__main__":
    input_path = os.path.join(Constants.INPUT_DIR, 'input.dwg')
    output_path = os.path.join(Constants.OUTPUT_DIR, 'output_test.csv')

    ds = DrawingScanner()
    document = ds.open_file(input_path)
    ms = ds.get_modelspace(document)
    ds.rotate_all_objs(document)
    data_dict = ds.search_blocks(ms)

    with open(output_path, mode='w', newline='') as csv_file:
        field_names = ['Blockname', 'Quantity', 'Length']
        writer = csv.DictWriter(csv_file, field_names)
        writer.writeheader()

        for key, value in data_dict.items():
            value_split = value.split('-')
            quantity = value_split[0]
            length = value_split[1]
            writer.writerow({'Blockname': key, 'Quantity': quantity, 'Length': length})
