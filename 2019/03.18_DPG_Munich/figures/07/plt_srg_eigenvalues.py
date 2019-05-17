"""Script to plot 3-body ground state energies for the SRG run."""
import glob
import json

import matplotlib
import matplotlib.pyplot as plt

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

# Create figure
fig1, ax1 = plt.subplots()

# Load file
file = glob.glob(path.format("t_rel*eigen*.json"))[0]
with open(file) as f:
    data = json.load(f)

# Get lambdas and values
lambdas = [float(key) for key in data]
vals = [data[key]["ho3"] for key in data]

# Plot data, once for points, one for the line
ax1.plot(lambdas, vals, "r.", label=r"$T_{rel}$")
ax1.plot(lambdas, vals, "r-")

# Load file
file = glob.glob(path.format("BlD*eigen*.json"))[0]
with open(file) as f:
    data = json.load(f)

# Get lambdas and values
lambdas = [float(key) for key in data]
vals = [data[key]["ho3"] for key in data]

# Plot data, once for points, one for the line
ax1.plot(lambdas, vals, "b.", label=r"Block")
ax1.plot(lambdas, vals, "b-")

# Set x-axis scale and ticks
ax1.set_xscale("log")
ax1.set_xticks([1, 2, 5, 10, 20, 50])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

# Set axis labels and title
plt.xlabel(r"$\lambda$ (fm$^{-1}$)")
plt.ylabel(r"$E_3$ (MeV)")
plt.title("3-Body Binding Energy", x=0.4, y=1.05)

# Set y-axis limits
plt.ylim(-3.0, -2.5)

# Enable legend
plt.legend(loc="lower right", fontsize="small")

# Adjust margins
plt.gcf().subplots_adjust(left=0.30)
plt.gcf().subplots_adjust(right=0.99)
plt.gcf().subplots_adjust(top=0.85)
plt.gcf().subplots_adjust(bottom=0.20)

# Set size of plot
plt.gcf().set_size_inches(1.6 * fig_height, 1.6 * fig_height)

# Save as PDF
plt.savefig("eigenvalues.pdf")
