"""Script to generate plot of series of potentials in SRG run."""
import glob
import json

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
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
path = './fig_data/{}'

# Set figure height
fig_height = 1.3

# Set maximum momentum to show
kmax = 12.0

# Set lambdas to show
lambdas = [50, 5.0, 3.0, 2.0, 1.5]

# Get file
file = glob.glob(path.format('*pot*.json'))
file = file[0]

# Load data
with open(file) as f:
    data = json.load(f)

# Get old nodes for data
data_nodes = np.array(data['nodes'])

# Define new even grid for data
nodes = np.linspace(0.0, kmax, 200)

# Set up initial figure
figure = plt.figure(1, (len(lambdas) * fig_height + fig_height/4, fig_height))

# Set up grid in figure
grid = ImageGrid(figure, 111, nrows_ncols=(1, len(lambdas)), axes_pad=0.0,
                 share_all=False, label_mode='L', cbar_location='right',
                 cbar_mode='single')

# Iterate over lambdas
for i, lam in enumerate(lambdas):
    # Read in potential
    potential = np.array(data['data'][str(lam)])

    # Interpolate potential
    interp = scipy.interpolate.RectBivariateSpline(data_nodes, data_nodes,
                                                   potential)
    potential = interp(nodes, nodes)

    # Plot potential matrix on corresponding axis in grid
    ax = grid[i]
    im = ax.matshow(potential, extent=[0.0, kmax, kmax, 0.0],
                    vmax=2, vmin=-2)

    # Set ticks for axes for this axis
    ax.set_xticks([0, 5, 10])
    ax.set_yticks([0, 5, 10])

    # Set xlabel on 3rd grid
    if i == 2:
        ax.set_xlabel(r"$k'$ (fm$^{-1}$)", labelpad=8)
        ax.xaxis.set_label_position('top')

    # Set ylabel on first grid
    if i == 0:
        ax.set_ylabel(r"$k$ (fm$^{-1}$)")

    # Add label for lambda value
    unit = r' fm$^{-1}$'
    if lam == 50:
        lam = r'\infty'
        unit = ''
    ax.text(1, 11, '$\\lambda = {}${}'.format(lam, unit))

    # Move xticks to top
    ax.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=True,
        labelbottom=False,
    )
    # Disable yticks for grids after the left most
    if i != 0:
        ax.tick_params(
            axis='y',
            which='both',
            left=False,
        )

# Set colorbar
grid.cbar_axes[0].colorbar(im)

# Set colorbar labels
for i, cax in enumerate(grid.cbar_axes):
    cax.set_yticks([-2, 0, 2])
    labels = [item.get_text() for item in cax.get_yticklabels()]
    labels = ['-2', '0', '']
    labels[-1] = r'2 (MeV)'
    cax.set_yticklabels(labels)

# Set xticks to top
plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=True,
    labelbottom=False,
)

# Adjust margins
#  plt.gcf().subplots_adjust(left=0.075)
plt.gcf().subplots_adjust(right=0.85)
plt.gcf().subplots_adjust(top=0.82)
plt.gcf().subplots_adjust(bottom=-0.08)

# Set size of plot
plt.gcf().set_size_inches(5.0 * fig_height, 1.2 * fig_height)

# Save as PDF
plt.savefig('potentials.pdf')

