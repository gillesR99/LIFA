import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
from scipy.optimize import curve_fit
import numpy as np

from tif_parser import parse_tif


# get data
# ----------
data_lst = []
data_lst.append(parse_tif("data/reference/000_ug_ml.tif", concentration=0, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/reference/010_ug_ml.tif", concentration=10, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/reference/030_ug_ml.tif", concentration=30, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/reference/050_ug_ml.tif", concentration=50, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/reference/070_ug_ml.tif", concentration=70, col_start=900, col_end=950, row_start=1630, row_end=1680))
data_lst.append(parse_tif("data/reference/100_ug_ml.tif", concentration=100, col_start=900, col_end=950, row_start=1630, row_end=1680))


measured_data_lst = []

img_030_jph = parse_tif("data/measured/030_ug_ml_jph.tif", concentration=30, col_start=900, col_end=950, row_start=1630, row_end=1680)
img_050_ssb = parse_tif("data/measured/050_ug_ml_ssb.tif", concentration=50, col_start=450, col_end=500, row_start=800, row_end=850)
img_050_grb = parse_tif("data/measured/grb.tif", concentration=50, col_start=450, col_end=500, row_start=800, row_end=850)
# our measured data is saved as 8bit unsigned values, we need to convert them
# to 16bit unsigned values (with scaling)
img_030_jph.data = img_030_jph.data.astype(np.uint8)
img_050_ssb.data = img_050_ssb.data.astype(np.uint8)
img_050_grb.data = img_050_grb.data.astype(np.uint8)

measured_data_lst.append(img_030_jph)
measured_data_lst.append(img_050_ssb)
measured_data_lst.append(img_050_grb)

# plot settings
# ----------
plt.rcParams["font.family"] = "monospace"  # use monospace font

fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)

color_grid = "#b8b8b8"

ax = fig.add_subplot(gs[0, 0])
# ax.xaxis.set_major_locator(MultipleLocator(10))
# ax.xaxis.set_minor_locator(MultipleLocator(5))
# ax.yaxis.set_major_locator(MultipleLocator(5000))
# ax.yaxis.set_minor_locator(MultipleLocator(500))

ax.xaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
ax.xaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)
ax.yaxis.grid(True, which="major", color=color_grid, alpha=1.0, ls="--", lw=0.75)
ax.yaxis.grid(True, which="minor", color=color_grid, alpha=0.5, ls="--", lw=0.50)

ax.set_title("Channel Intensity over Concentration")
ax.set_xlabel(r"CRP Concentration $[\frac{\mu g}{mL}]$")
ax.set_ylabel("Green Channel Intensity")
# ax.set_xlim(-2, 102)
# ax.set_ylim(6000, 16000)


# data plot
# ----------

# boxplot
labels = []
colors = []
boxplot_data = []
data_mean = np.zeros(len(data_lst))

# reference data boxplot
for idx, data_struct in enumerate(data_lst):
    labels.append(data_struct.concentration)
    colors.append("blue")
    boxplot_data.append(data_struct.data[:, :, 1].flatten()*((2**8-1)/(2**14-1)))
    data_mean[idx] = data_struct.data[:,:,1].mean()*((2**8-1)/(2**14-1))

# measured data boxplot
for idx, data_struct in enumerate(measured_data_lst):
    labels.append(data_struct.concentration)
    colors.append("green")
    boxplot_data.append(data_struct.data[:, :, 1].flatten())

bp = ax.boxplot(boxplot_data,
                showbox=True, showcaps=True, showmeans=False, showfliers=False,
                widths=1,
                # label=f"{data_struct.concentration: 3}",
                tick_labels=labels,
                positions=labels)

# set color of median bar
for median_line, color in zip(bp["medians"], colors):
    median_line.set(color = color, linewidth = 2)


# fit
def sigmoid(x, L, x0, k, b):
    """
    x := x-axis
    L := scale y
    x0 := center of x-axis
    k := scale x
    b := shift y
    """
    y = (L / (1 + np.exp(-k*(x-x0)))) + b
    return y

p0 = [data_mean.max()-data_mean.min(), 25, 0.1, data_mean.min()]  # initial guesses for L, x0, k and b
popt, pcov = curve_fit(sigmoid, labels[:-len(measured_data_lst)], data_mean, p0,
                       bounds=((          p0[0],   0, p0[2]-1,     0),
                               (data_mean.max(), 100, p0[2]+1, p0[3])),
                       method="trf")

x_fit = np.linspace(0, 100, 100, dtype=int)
fit = sigmoid(x_fit, *popt)

ax.plot(x_fit, fit, color="red")


ref_patch = mpatches.Patch(color='blue', label='reference')
meas_patch = mpatches.Patch(color='green', label='measured')
fit_patch = mpatches.Patch(color='red', label='fit')
ax.legend(handles=[ref_patch, meas_patch, fit_patch], loc="upper left")
# display
plt.show()
