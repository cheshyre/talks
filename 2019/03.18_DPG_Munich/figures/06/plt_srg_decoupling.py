"""Script to plot decoupling data for an SRG evolution."""
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
path = './fig_data/{}'

# Height for figure
fig_height = 1.3

# Load file
file = glob.glob(path.format('*decoupling.json'))[0]
with open(file) as f:
    data = json.load(f)

# Read out lambdas and values
lambdas = [float(key) for key in data]
vals = [data[key]['ho'] for key in data]

# Create plot
fig1, ax1 = plt.subplots()

# Plot data
ax1.plot(lambdas, vals, 'r.')

# Set x-axis scale and ticks
ax1.set_xscale('log')
ax1.set_xticks([1, 2, 5, 10, 20, 50])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

# Set y-axis limits
plt.ylim((0, 34))

# Set labels and titles
plt.xlabel(r'$\lambda$ (fm$^{-1}$)')
plt.ylabel(r'$N_{max}$')
plt.title('Decoupling', x=0.45, y=1.05)

# Adjust margins
plt.gcf().subplots_adjust(left=0.23)
plt.gcf().subplots_adjust(right=0.92)
plt.gcf().subplots_adjust(top=0.85)
plt.gcf().subplots_adjust(bottom=0.20)

# Set size of plot
plt.gcf().set_size_inches(1.6 * fig_height, 1.6 * fig_height)

# Save as PDF
plt.savefig('decoupling.pdf')
