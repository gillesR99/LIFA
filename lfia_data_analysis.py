import numpy as np
import matplotlib.pyplot as plt
import scipy

from tif_parser import parse_tif


# read data
# ----------
img_030_left = parse_tif("data/measured/030_ug_ml_jph_left.tif", concentration=30)
img_030_center = parse_tif("data/measured/030_ug_ml_jph.tif", concentration=30)
img_030_right = parse_tif("data/measured/030_ug_ml_jph_right.tif", concentration=30)

img_050_1 = parse_tif("data/measured/050_ug_ml_ssb.tif", concentration=50)
img_050_2 = parse_tif("data/measured/050_ug_ml_ssb_2.tif", concentration=50)
img_050_3 = parse_tif("data/measured/050_ug_ml_ssb_3.tif", concentration=50)

img_ref_000 = parse_tif("data/reference/000_ug_ml.tif", concentration=0)
img_ref_010 = parse_tif("data/reference/010_ug_ml.tif", concentration=10)
img_ref_030 = parse_tif("data/reference/030_ug_ml.tif", concentration=30)
img_ref_050 = parse_tif("data/reference/050_ug_ml.tif", concentration=50)
img_ref_070 = parse_tif("data/reference/070_ug_ml.tif", concentration=70)
img_ref_100 = parse_tif("data/reference/100_ug_ml.tif", concentration=100)

# our measured data is saved as 8bit unsigned values, we need to convert them
# to 16bit unsigned values (with scaling)
img_030_left.data = img_030_left.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_030_center.data = img_030_center.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_030_right.data = img_030_right.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_1.data = img_050_1.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_2.data = img_050_2.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_3.data = img_050_3.data.astype(np.uint16) * ((2**16-1)/(2**8-1))

breakpoint()
