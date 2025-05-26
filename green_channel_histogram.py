import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

from tif_parser import parse_tif


# get data
# ----------
data_lst = []
data_lst.append(parse_tif("data/measured/030_ug_ml_jph_left.tif", concentration=30))
# data_lst.append(parse_tif("data/measured/030_ug_ml_jph.tif", concentration=30, col_start=900, col_end=950, row_start=1630, row_end=1680))
# data_lst.append(parse_tif("data/measured/030_ug_ml_jph_right.tif", concentration=30, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/measured/050_ug_ml_ssb.tif", concentration=50))
# data_lst.append(parse_tif("data/measured/050_ug_ml_ssb_2.tif", concentration=50, col_start=900, col_end=950, row_start=1630, row_end=1680))
# data_lst.append(parse_tif("data/measured/050_ug_ml_ssb_3.tif", concentration=50, col_start=900, col_end=950, row_start=1630, row_end=1680))



# data_lst.append(parse_tif("data/measured/grb.tif", concentration=50, col_start=450, col_end=500, row_start=800, row_end=850))
# data_lst.append(parse_tif("data/measured/grb_2.tif", concentration=50, col_start=450, col_end=500, row_start=800, row_end=850))
# data_lst.append(parse_tif("data/measured/grb_3.tif", concentration=50, col_start=450, col_end=500, row_start=800, row_end=850))



# data_lst.append(parse_tif("data/reference/000_ug_ml.tif", concentration=0))
# data_lst.append(parse_tif("data/reference/010_ug_ml.tif", concentration=10))
data_lst.append(parse_tif("data/reference/030_ug_ml.tif", concentration=30))
data_lst.append(parse_tif("data/reference/050_ug_ml.tif", concentration=50))
# data_lst.append(parse_tif("data/reference/070_ug_ml.tif", concentration=70))
# data_lst.append(parse_tif("data/reference/100_ug_ml.tif", concentration=100))

# plot settings
# ----------
plt.rcParams["font.family"] = "monospace"  # use monospace font

fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)

color_grid = "#b8b8b8"

hist_030 = fig.add_subplot(gs[0, 0])
hist_050 = fig.add_subplot(gs[1, 0])
# hist_050_1 = fig.add_subplot(gs[2, 0])

# histo.xaxis.set_major_locator(MultipleLocator(10))
# histo.xaxis.set_minor_locator(MultipleLocator(5))
# histo.yaxis.set_major_locator(MultipleLocator(1000))
# histo.yaxis.set_minor_locator(MultipleLocator(100))

hist_030.xaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
hist_030.xaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)
hist_030.yaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
hist_030.yaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)

hist_030.set_title("Green Channel Histogram 30, complete image")
hist_030.set_xlabel(r"Green Channel Intensity")
hist_030.set_ylabel("# of Pixels")
hist_030.set_xlim(0, 256)

hist_050.xaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
hist_050.xaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)
hist_050.yaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
hist_050.yaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)

hist_050.set_title("Green Channel Histogram 50, complete image")
hist_050.set_xlabel(r"Green Channel Intensity")
hist_050.set_ylabel("# of Pixels")
hist_050.set_xlim(0, 256)

# hist_050_1.xaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
# hist_050_1.xaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)
# hist_050_1.yaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
# hist_050_1.yaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)

# hist_050_1.set_title("Green Channel Histogram 50")
# hist_050_1.set_xlabel(r"Green Channel Intensity")
# hist_050_1.set_ylabel("# of Pixels")
# hist_050_1.set_xlim(0, 256)

# boxplot
labels = []
green_channel_historgamm_data = []
for data_struct in data_lst:
    labels.append(data_struct.concentration)
    green_channel_historgamm_data.append(data_struct.data[:, :, 0].flatten()*0.299+data_struct.data[:, :, 1].flatten()*0.587+data_struct.data[:, :, 2].flatten()*0.114)


gch_data_030 = []
gch_data_050 = []
gch_data_050_1 = []

gch_data_030.extend(green_channel_historgamm_data[0])
gch_data_050.extend(green_channel_historgamm_data[1])
gch_data_050_1.extend(green_channel_historgamm_data[2])

#hist_030.hist([gch_data_030, green_channel_historgamm_data[9]/((2**16-1)/(2**8-1))],
#              bins=[100,100] , color=['green', 'blue'], edgecolor=['darkgreen', 'darkblue'])
#hist_050.hist([gch_data_050, green_channel_historgamm_data[10]],
#              bins=[100,100] , color=['green','blue'], edgecolor=['darkgreen', 'darkblue'])

hist_030.hist(gch_data_030,
              bins=100, color='green', edgecolor='darkgreen', label="measured")
hist_030.hist([green_channel_historgamm_data[2]*((2**8-1)/(2**14-1))],
              bins=30, color='blue', edgecolor='darkblue', label="reference")

hist_050.hist(gch_data_050,
              bins=100, color='green', edgecolor='darkgreen', label="measured")
hist_050.hist([green_channel_historgamm_data[3]*((2**8-1)/(2**14-1))],
              bins=30, color='blue', edgecolor='darkblue', label="reference")

# hist_050_1.hist(gch_data_050_1 , bins=100 , color='green', edgecolor='darkgreen', label="measured")

# hist_050_1.hist([green_channel_historgamm_data[4]*((2**8-1)/(2**14-1))],
#               bins=30, color='blue', edgecolor='darkblue', label="reference")

hist_030.legend(loc="upper left")
hist_050.legend(loc="upper left")
# hist_050_1.legend(loc="upper left")

mean_m30 = np.mean([gch_data_030])
mean_m50 = np.mean([gch_data_050])
mean_r30 = np.mean([green_channel_historgamm_data[2]*((2**8-1)/(2**14-1))])
mean_r50 = np.mean([green_channel_historgamm_data[3]*((2**8-1)/(2**14-1))])

print(mean_m30)
print(mean_m50)
print(mean_r30)
print(mean_r50)
# display
plt.show()
