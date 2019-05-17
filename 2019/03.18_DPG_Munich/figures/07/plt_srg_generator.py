"""Script to plot generator for SRG run."""
import glob
import json

import matplotlib
import matplotlib.pyplot as plt
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

# Set path for data
# pylint: disable=C0103
path = "./fig_data/{}"

# Height for figure
fig_height = 1.3

# Set maximum momentum to show in matrix
kmax = 12.0

# Get file
file = glob.glob(path.format("*pot*.json"))
file = file[0]

# Load data
with open(file) as f:
    data = json.load(f)

# Get old nodes for data
data_nodes = np.array(data["nodes"])

# Define new even grid for data
nodes = np.linspace(0.0, kmax, 40)

# Set up generator data
generator = np.array(data["generator"])
interp = scipy.interpolate.RectBivariateSpline(
    data_nodes, data_nodes, generator
)
generator_interp = -1 * interp(nodes, nodes)
for i in range(len(generator_interp)):
    generator_interp[i][i] = 1.0

# Create figure
fig, ax = plt.subplots()

# Plot matrix
ax.matshow(
    generator_interp,
    extent=[0, kmax, kmax, 0],
    vmax=1,
    vmin=-1,
    cmap=plt.get_cmap("bwr"),
)

# Set axis ticks
ax.set_xticks([0, 5, 10])
ax.set_yticks([0, 5, 10])

# Set x axis ticks to be on the bottom
ax.tick_params(
    axis="x",
    which="both",
    bottom=True,
    top=False,
    labelbottom=True,
    labeltop=False,
)

# Set axis labels and title
plt.xlabel(r"$k'$ (fm$^{-1}$)")
plt.ylabel(r"$k$ (fm$^{-1}$)")
plt.title("Generator Form", x=0.5, y=1.05)

# Adjust margins
# plt.gcf().subplots_adjust(left=0.075)
plt.gcf().subplots_adjust(right=1.05)
plt.gcf().subplots_adjust(top=0.85)
plt.gcf().subplots_adjust(bottom=0.20)

# Set size of plot
plt.gcf().set_size_inches(1.5 * fig_height, 1.6 * fig_height)

# Save as PDF
plt.savefig("generator.pdf")
