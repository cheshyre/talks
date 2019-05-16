"""Script to plot 2 potentials stacked."""
import json
import glob

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import scipy.interpolate


# matplotlib font configurations
matplotlib.rcParams["text.latex.preamble"] = [
    # i need upright \micro symbols, but you need...
    r"\usepackage{siunitx}",
    # ...this to force siunitx to actually use your fonts
    r"\sisetup{detect-all}",
    # set the normal font here
    r"\usepackage{helvet}",
    # load up the sansmath so that math -> helvet
    r"\usepackage{sansmath}",
    # <- tricky! -- gotta actually tell tex to use!
    r"\sansmath",
]

# Use tex for matplotlib
plt.rc("text", usetex=True)

# pylint: disable=C0103
# Load path for data
path = "./fig_data/{}"

# Maximum momentum to show
kmax = 12.0

# Figure height
fig_height = 1.6

# Get file
file = glob.glob(path.format("*pot*.json"))
file = file[0]

# Load data
with open(file) as f:
    data = json.load(f)

# Get old nodes for data
data_nodes = np.array(data["nodes"])

# Define new even grid for data
nodes = np.linspace(0.0, kmax, 200)

# Read out potential and interpolate to new grid
orig_potential = np.array(data["data"][str(50)])
interp = scipy.interpolate.RectBivariateSpline(
    data_nodes, data_nodes, orig_potential
)
orig_potential = interp(nodes, nodes)

# Read out evolved potential and interpolate to new grid
evolved_potential = np.array(data["data"][str(1.5)])
interp = scipy.interpolate.RectBivariateSpline(
    data_nodes, data_nodes, evolved_potential
)
evolved_potential = interp(nodes, nodes)

# Create basic figure
fig = plt.figure(figsize=(0.6 * fig_height, fig_height))

# Set up grid: 2x2 for 2 stacked matrix plots and a shared color bar
gs1 = gridspec.GridSpec(2, 2, height_ratios=(1, 1), width_ratios=(20, 1))
gs1.update(hspace=0, wspace=0)

# Extract axes for relevant subplots in the grid
ax1 = fig.add_subplot(gs1[0, 0])
ax2 = fig.add_subplot(gs1[1, 0])
ax3 = fig.add_subplot(gs1[:, 1])

# Plot original and evolved potentials as matrices
mat = ax1.matshow(
    orig_potential, extent=[0.0, kmax, kmax, 0.0], vmax=2, vmin=-2
)
ax2.matshow(evolved_potential, extent=[0.0, kmax, kmax, 0.0], vmax=2, vmin=-2)

# Set ticks on axes
ax1.set_xticks([0, 5, 10])
ax2.set_xticks([])
ax1.set_yticks([0, 5, 10])
ax2.set_yticks([0, 5, 10])

# Show color bar
cax = plt.colorbar(mat, cax=ax3)

# Set ticks on colorbar, overriding labels to include MeV units
cax.set_ticks([-2, 0, 2])
labels = ["-2", "0", ""]
labels[-1] = r"2 (MeV)"
cax.set_ticklabels(labels)

# Specify that only ax1 should have x ticks on top
ax2.tick_params(
    axis="x", which="both", bottom=False, top=False, labelbottom=False
)
ax1.tick_params(
    axis="x", which="both", bottom=False, top=True, labelbottom=False
)

# Set xlabel
ax1.set_xlabel(r"$k'$ (fm$^{-1}$)", labelpad=8)
ax1.xaxis.set_label_position("top")

# Set ylabel
ax2.set_ylabel(r"$k$ (fm$^{-1}$)", y=1)

# Add additional labels for the different subplots
ax1.text(1, 11, r"$\lambda = \infty$")
ax2.text(1, 11, r"$\lambda = 1.5$ fm$^{-1}$")

# Adjust positions of subplots
plt.gcf().subplots_adjust(left=0.24)
plt.gcf().subplots_adjust(right=0.715)
plt.gcf().subplots_adjust(top=0.80)
plt.gcf().subplots_adjust(bottom=0.05)

# Set size of plot
plt.gcf().set_size_inches(1.5 * fig_height, 1.8 * fig_height)

# Save as PDF
plt.savefig("srg_potentials.pdf")
