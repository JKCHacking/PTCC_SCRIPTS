from src.dxf_2_gcode import DXF2Gcode

if __name__ == "__main__":

    script = DXF2Gcode()
    for file in script.iter_input():
        for ent in script.read_dxf(file):
            pass




