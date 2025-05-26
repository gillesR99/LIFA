# Parser for the openmicroscopy TIF file format, used in the LFIA lab
# https://ome-model.readthedocs.io/en/stable/specifications/index.html#definitions-of-values-stored

import numpy as np
import tifffile as tiff
from dataclasses import dataclass
import re

@dataclass
class Img_data:
    file_name: str = ""
    data: np.ndarray = None
    roi: dict = None
    resolution: int = None
    exposure_time: float = None  # [s]
    concentration: float = None  # [ug/mL]
    gain: float = None
    significant_bits: int = None


def parse_tif(file_path: str, concentration: float,
              col_start: int = 0, col_end: int = None,
              row_start: int = 0, row_end: int = None) -> Img_data:

    img_data = Img_data()
    img_data.file_name = file_path

    with tiff.TiffFile(file_path) as tif_file:

        # we only have one page
        tif_page = tif_file.pages[0]

        # get data
        img_data.data = tif_page.asarray()[col_start:col_end, row_start:row_end, :]
        img_data.roi = {"col": [col_start, col_start + img_data.data.shape[0]],
                        "row": [row_start, row_start + img_data.data.shape[1]]}

        img_data.resolution = tif_page.tags["BitsPerSample"].value[0]
        meta_data = tif_page.tags["ExifTag"].value
        img_data.exposure_time = meta_data["ExposureTime"][0] / meta_data["ExposureTime"][1]
        img_data.concentration = concentration

        # gain
        gain_start_idx = tif_page.tags["ImageDescription"].value.find("Gain")
        img_data.gain = float(tif_page.tags["ImageDescription"].value[gain_start_idx+6:gain_start_idx+24])

        # significant bits
        significant_bits_start_idx = tif_page.tags["ImageDescription"].value.find("SignificantBits")
        significant_bit_sub_str = tif_page.tags["ImageDescription"].value[significant_bits_start_idx:significant_bits_start_idx+30]  # needed substring should be within 30 chars
        img_data.significant_bits = int(re.search(r'\d+', significant_bit_sub_str).group())

    return img_data


def print_tags(file_path: str) -> None:

    img_data = Img_data()
    img_data.file_name = file_path

    with tiff.TiffFile(file_path) as tif_file:

        # we only have one page
        tif_page = tif_file.pages[0]

        for tag in tif_page.tags:
            print(f"{tag.name} : {tag.value}")


if __name__ == "__main__":
    file_path = "data/measured/030_ug_ml_jph_right.tif"
    file_path_ref = "data/reference/030_ug_ml.tif"

    img_obj = parse_tif(file_path, concentration=30, row_start = 5, col_start = 10)
    img_obj_ref = parse_tif(file_path_ref, concentration=30)

    print("")
    print(f"                  | {'measured':^9} | {'reference':^19} |")
    print("-"*62)
    print(f" exposure time    | {img_obj.exposure_time:>9} | {img_obj_ref.exposure_time} | [s]")
    print(f" resolution       | {img_obj.resolution:>9} | {img_obj_ref.resolution:>19} | [bits]")
    print(f" significant bits | {img_obj.significant_bits:>9} | {img_obj_ref.significant_bits:>19} | [bits]")
    print(f" concentration    | {img_obj.concentration:>9} | {img_obj_ref.concentration:>19} | [ug/mL]")
    print(f" gain             | {img_obj.gain:>9} | {img_obj_ref.gain:>19} |")
    print(f" ROI columns      | {str(img_obj.roi['col']):>9} | {str(img_obj_ref.roi['col']):>19} | [px]")
    print(f" ROI rows         | {str(img_obj.roi['row']):>9} | {str(img_obj_ref.roi['row']):>19} | [px]")
    print("")


