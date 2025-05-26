import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

from tif_parser import parse_tif


# get data
# ----------
img_030_left = parse_tif("data/measured/030_ug_ml_jph_left.tif", concentration=30)
img_030_center = parse_tif("data/measured/030_ug_ml_jph.tif", concentration=30)
img_030_right = parse_tif("data/measured/030_ug_ml_jph_right.tif", concentration=30)

img_050_1 = parse_tif("data/measured/050_ug_ml_ssb.tif", concentration=50)
img_050_2 = parse_tif("data/measured/050_ug_ml_ssb_2.tif", concentration=50)
img_050_3 = parse_tif("data/measured/050_ug_ml_ssb_3.tif", concentration=50)

img_ref_030 = parse_tif("data/reference/030_ug_ml.tif", concentration=30)
img_ref_050 = parse_tif("data/reference/050_ug_ml.tif", concentration=50)

# our measured data is saved as 8bit unsigned values, we need to convert them
# to 16bit unsigned values (with scaling)
img_030_left.data = img_030_left.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_030_center.data = img_030_center.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_030_right.data = img_030_right.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_1.data = img_050_1.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_2.data = img_050_2.data.astype(np.uint16) * ((2**16-1)/(2**8-1))
img_050_3.data = img_050_3.data.astype(np.uint16) * ((2**16-1)/(2**8-1))

# prepare data for boxplot
meas_red_data_050 = np.concat((img_050_1.data[:, :, 0],
                               img_050_2.data[:, :, 0],
                               img_050_3.data[:, :, 0])).flatten()
meas_green_data_050 = np.concat((img_050_1.data[:, :, 1],
                                 img_050_2.data[:, :, 1],
                                 img_050_3.data[:, :, 1])).flatten()
meas_blue_data_050 = np.concat((img_050_1.data[:, :, 2],
                                img_050_2.data[:, :, 2],
                                img_050_3.data[:, :, 2])).flatten()

meas_red_data_030 = np.concat((img_030_left.data[:, :, 0],
                               img_030_center.data[:, :, 0],
                               img_030_right.data[:, :, 0])).flatten()
meas_green_data_030 = np.concat((img_030_left.data[:, :, 1],
                                 img_030_center.data[:, :, 1],
                                 img_030_right.data[:, :, 1])).flatten()
meas_blue_data_030 = np.concat((img_030_left.data[:, :, 2],
                                img_030_center.data[:, :, 2],
                                img_030_center.data[:, :, 2])).flatten()

# plot settings
# ----------
plt.rcParams["font.family"] = "monospace"  # use monospace font

fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)

color_grid = "#b8b8b8"

hist_meas_030 = fig.add_subplot(gs[0, 0])
hist_ref_030 = fig.add_subplot(gs[1, 0])
hist_meas_050 = fig.add_subplot(gs[0, 1])
hist_ref_050 = fig.add_subplot(gs[1, 1])

# same settings for all plots
ax_lst = [hist_meas_030, hist_ref_030, hist_meas_050, hist_ref_050]
title_lst = ["Measured Data 30", "Reference Data 30", "Measured Data 50", "Reference Data 50"]
for idx in range(4):
    ax_lst[idx].xaxis.set_major_locator(MultipleLocator(2**13))
    ax_lst[idx].xaxis.grid(True, which="major", color=color_grid,
                           alpha=1.0, ls="--", lw=0.75)
    ax_lst[idx].xaxis.grid(True, which="minor", color=color_grid,
                           alpha=0.5, ls="--", lw=0.50)
    ax_lst[idx].yaxis.grid(True, which="major", color=color_grid,
                           alpha=1.0, ls="--", lw=0.75)
    ax_lst[idx].yaxis.grid(True, which="minor", color=color_grid,
                           alpha=0.5, ls="--", lw=0.50)

    ax_lst[idx].set_title(title_lst[idx])
    ax_lst[idx].set_xlabel(r"Channel Intensity")
    ax_lst[idx].set_ylabel("# of Pixels")
    ax_lst[idx].set_xlim(-100, 2**16)
    ax_lst[idx].set_ylim(0, 600000)


# boxplot
# ----------
hist_meas_030.hist(meas_red_data_030,
               bins=100, color='red', edgecolor='darkred', label="measured")
hist_meas_030.hist(meas_green_data_030,
               bins=100, color='green', edgecolor='darkgreen', label="measured")
hist_meas_030.hist(meas_blue_data_030,
               bins=100, color='blue', edgecolor='darkblue', label="measured")

hist_ref_030.hist(img_ref_030.data[:, :, 0].flatten(),
              bins=30, color='red', edgecolor='darkred', label="reference")
hist_ref_030.hist(img_ref_030.data[:, :, 1].flatten(),
              bins=30, color='green', edgecolor='darkgreen', label="reference")
hist_ref_030.hist(img_ref_030.data[:, :, 2].flatten(),
              bins=30, color='blue', edgecolor='darkblue', label="reference")

hist_meas_050.hist(meas_red_data_050,
               bins=100, color='red', edgecolor='darkred', label="measured")
hist_meas_050.hist(meas_green_data_050,
               bins=100, color='green', edgecolor='darkgreen', label="measured")
hist_meas_050.hist(meas_blue_data_050,
               bins=100, color='blue', edgecolor='darkblue', label="measured")

hist_ref_050.hist(img_ref_050.data[:, :, 0].flatten(),
              bins=30, color='red', edgecolor='darkred', label="reference")
hist_ref_050.hist(img_ref_050.data[:, :, 1].flatten(),
              bins=30, color='green', edgecolor='darkgreen', label="reference")
hist_ref_050.hist(img_ref_050.data[:, :, 2].flatten(),
              bins=30, color='blue', edgecolor='darkblue', label="reference")

# boxplot for percentage
# ----------
# bins = 100
#
# counts, bin = np.histogram(meas_red_data, density=False, bins=bins)
# hist_meas.stairs(counts/counts.sum()*100, bin, fill=True, color="red")
# counts, bin = np.histogram(meas_green_data, density=False, bins=bins)
# hist_meas.stairs(counts/counts.sum()*100, bin, fill=True, color="green")
# counts, bin = np.histogram(meas_blue_data, density=False, bins=bins)
# hist_meas.stairs(counts/counts.sum()*100, bin, fill=True, color="blue")
#
# counts, bin = np.histogram(img_ref_050.data[:, :, 0].flatten(), density=False, bins=bins)
# hist_ref.stairs(counts/counts.sum()*100, bin, fill=True, color="red")
# counts, bin = np.histogram(img_ref_050.data[:, :, 1].flatten(), density=False, bins=bins)
# hist_ref.stairs(counts/counts.sum()*100, bin, fill=True, color="green")
# counts, bin = np.histogram(img_ref_050.data[:, :, 2].flatten(), density=False, bins=bins)
# hist_ref.stairs(counts/counts.sum()*100, bin, fill=True, color="blue")

# display
# ----------
plt.show()
