import json
import glob
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib


matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]
plt.rc('text', usetex=True)


kmax = 12.0
path = './fig_data/{}'

fig_height = 1.6

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

orig_potential = np.array(data['data'][str(50)])
interp = scipy.interpolate.RectBivariateSpline(data_nodes, data_nodes,
                                               orig_potential)
orig_potential = interp(nodes, nodes)
evolved_potential = np.array(data['data'][str(1.5)])
interp = scipy.interpolate.RectBivariateSpline(data_nodes, data_nodes,
                                               evolved_potential)
evolved_potential = interp(nodes, nodes)

fig=plt.figure(figsize=(0.6 * fig_height, fig_height))
gs1 = gridspec.GridSpec(2, 2, height_ratios=(1, 1), width_ratios=(20, 1))
gs1.update(hspace=0, wspace=0)
ax1 = fig.add_subplot(gs1[0, 0])
ax2 = fig.add_subplot(gs1[1, 0])
ax3 = fig.add_subplot(gs1[:, 1])
mat = ax1.matshow(orig_potential, extent=[0.0, kmax, kmax, 0.0], vmax=2, vmin=-2)
ax2.matshow(evolved_potential, extent=[0.0, kmax, kmax, 0.0], vmax=2, vmin=-2)
ax1.set_xticks([0, 5, 10])
ax2.set_xticks([])
ax1.set_yticks([0, 5, 10])
ax2.set_yticks([0, 5, 10])
cax = plt.colorbar(mat, cax=ax3)
cax.set_ticks([-2, 0, 2])
labels = ['-2', '0', '']
labels[-1] = r'2 (MeV)'
cax.set_ticklabels(labels)
ax2.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=False,
    labelbottom=False,
)
ax1.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=True,
    labelbottom=False,
)
ax1.set_xlabel(r"$k'$ (fm$^{-1}$)", labelpad=8)
ax1.xaxis.set_label_position('top')
ax2.set_ylabel(r'$k$ (fm$^{-1}$)', y=1)
ax1.text(1, 11, r'$\lambda = \infty$')
ax2.text(1, 11, r'$\lambda = 1.5$ fm$^{-1}$')
#      if i != 0:
#          ax.set_xticklabels(['', '', ''])
#      else:
#          ax.set_xticklabels(['0', '5', '10'])
#      if i == 0:
#          ax.set_xlabel(r"$k'$ (fm$^{-1}$)")
#          ax.xaxis.set_label_position('top')
#      if i == 0:
#          ax.set_ylabel(r"$k$ (fm$^{-1}$)")
#      if lam == 50:
#          lam = '\\infty'
#      ax.text(1, 11, '$\\lambda = {}$'.format(lam))
#
#      if i != 0:
#          ax.tick_params(
#              axis='x',
#              which='both',
#              bottom=False,
#              top=False,
#              labelbottom=False,
#          )
#      else:
#          ax.tick_params(
#              axis='x',
#              which='both',
#              bottom=False,
#              top=True,
#              labelbottom=False,
#          )
#      ax.tick_params(
#          axis='y',
#          which='both',
#          left=True,
#      )
#
#  #  for i, ax in enumerate(grid.axes_all):
#  #      labels = ax.get_xticklabels()
#  #      labels[-1] = ''
#  #      if
#  #      ax.set_xticklabels(labels)
#
#
#  #  grid.cbar_axes[0].colorbar(im)
#
#  #  for i, cax in enumerate(grid.cbar_axes):
#      #  cax.set_yticks([-2, 0, 2])
#      #  labels = [item.get_text() for item in cax.get_yticklabels()]
#      #  labels = ['-2', '0', '']
#      #  labels[-1] = r'2 (MeV)'
#      #  cax.set_yticklabels(labels)
#  #
#  #  plt.tick_params(
#  #      axis='x',
#  #      which='both',
#  #      bottom=False,
#  #      top=True,
#  #      labelbottom=False,
#  #  )
#  plt.xlabel(r"$k'$ (fm$^{-1}$)")
plt.gcf().subplots_adjust(left=0.24)
plt.gcf().subplots_adjust(right=0.715)
plt.gcf().subplots_adjust(top=0.80)
plt.gcf().subplots_adjust(bottom=0.05)
plt.gcf().set_size_inches(1.5 * fig_height, 1.8 * fig_height)
plt.savefig('srg_potentials.pdf')

