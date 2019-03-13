import json
import glob
import scipy.interpolate
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from mpl_toolkits.axes_grid1 import ImageGrid

matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]
plt.rc('text', usetex=True)


kmax = 12.0
lambdas = [50, 5.0, 3.0, 2.0, 1.5]
#  path = 'data/BlockDiag_soft_1.5_0.2_*/{}'
path = 'data/BandDiag_soft_1.25_0.2_*/{}'
path = 'data/T_rel_*/{}'
path = './fig_data/{}'
fig_height = 1.3


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

for i, lam in enumerate(lambdas):
    potential = np.array(data['data'][str(lam)])

    interp = scipy.interpolate.RectBivariateSpline(data_nodes, data_nodes,
                                                   potential)

    potential = interp(nodes, nodes)

    ax = grid[i]

    im = ax.matshow(potential, extent=[0.0, kmax, kmax, 0.0],
                    vmax=2, vmin=-2)
    #  if i != 0:
        #  print(labels[-1])
        #  #  labels[-1] = ''
        #  print(labels)
    ax.set_xticks([0, 5, 10])
    ax.set_yticks([0, 5, 10])
    if i == 2:
        ax.set_xlabel(r"$k'$ (fm$^{-1}$)")
        ax.xaxis.set_label_position('top')
    if i == 0:
        ax.set_ylabel(r"$k$ (fm$^{-1}$)")
    if lam == 50:
        lam = '\\infty'
    ax.text(1, 11, '$\\lambda = {}$'.format(lam))

    ax.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=True,
        labelbottom=False,
    )
    if i != 0:
        ax.tick_params(
            axis='y',
            which='both',
            left=False,
        )

#  for i, ax in enumerate(grid.axes_all):
#      labels = ax.get_xticklabels()
#      labels[-1] = ''
#      if
#      ax.set_xticklabels(labels)


grid.cbar_axes[0].colorbar(im)

for i, cax in enumerate(grid.cbar_axes):
    cax.set_yticks([-2, 0, 2])
    labels = [item.get_text() for item in cax.get_yticklabels()]
    labels = ['-2', '0', '']
    labels[-1] = r'2 (MeV)'
    cax.set_yticklabels(labels)

plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=True,
    labelbottom=False,
)
plt.xlabel(r"$k'$ (fm$^{-1}$)")
#  plt.gcf().subplots_adjust(left=0.075)
plt.gcf().subplots_adjust(right=0.85)
plt.gcf().subplots_adjust(top=0.85)
plt.gcf().subplots_adjust(bottom=-0.05)
plt.gcf().set_size_inches(5.0 * fig_height, 1.2 * fig_height)
plt.savefig('potentials.pdf')

