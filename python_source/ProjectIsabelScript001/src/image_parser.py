import os
import re
import datetime
import math
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from src.constants import Constants


class ImageParser:
    def __init__(self):
        self.input_dir = Constants.INPUT_DIR

    def parse_image(self):
        count = 0
        # iterate in input folder
        for dir_path, dir_names, file_names in os.walk(self.input_dir):
            for file_name in file_names:

                if file_name.endswith(Constants.TIF_EXT):
                    image_full_path = os.path.join(dir_path, file_name)
                    file_name = Path(file_name).stem

                    file_name_split = file_name.split("_")
                    month = int(file_name_split[0])
                    day = int(file_name_split[1])
                    time = file_name_split[2]
                    time = int(time.replace('p', '.'))

                    dec, whole = math.modf(time)
                    hour = int(whole)
                    minutes = math.ceil(dec * 60)
                    time_obj = datetime.time(hour=hour, minute=minutes)

                    # MANILA
                    lat = 14.58300
                    long = -120.983
                    mer = -120.0
                    rad_command = f'C:/Radiance/bin/gensky.exe {month} {day} {time} -a {lat} -o {long} -m {mer}'

                    stream = os.popen(rad_command)
                    output = stream.read()
                    re_result = re.search('Solar altitude and azimuth: -*\d{1,2}.[0-9] -*\d{1,2}.[0-9]', output)
                    solar_coord_string = re_result.group(0)
                    re_result = re.search('-*\d{1,2}.[0-9] -*\d{1,2}.[0-9]', solar_coord_string)
                    solar_coord_val_str = re_result.group(0)
                    solar_alt, azimuth = solar_coord_val_str.split(" ")
                    azimuth = (float(azimuth) - 180) * -1
                    count += 1
                    print(f'{count} {solar_coord_string}')
                    print(solar_alt)
                    print(azimuth)

                    # date = f'{Constants.MONTH_NAME[month-1]} {day}'
                    date = f'{Constants.MONTH_NAME[month-1]}'
                    ref = '100'
                    self.__put_text(image_full_path, date, time_obj.strftime(Constants.TIME_24_FORMAT),
                                    solar_alt, azimuth, ref)

    def __put_text(self, image_path, date, time, solar_alt, azimuth, reflectivity):
        image_dir = os.path.dirname(image_path)
        filename = Path(image_path).stem

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font_size = 12
        font = ImageFont.truetype('arial.ttf', font_size)
        draw.text((0, 0),
                  f"Date: {date}\nTime: {time}\nSolar Altitude: {solar_alt}\xB0\nAzimuth: {azimuth}\xB0\n" +
                  f"Reflectivity: {reflectivity}%", (255, 255, 255), font=font)
        save_path = os.path.join(image_dir, filename + ".tif")
        image.save(save_path)
