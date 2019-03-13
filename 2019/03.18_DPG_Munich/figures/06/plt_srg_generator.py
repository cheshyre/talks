import json
import glob
import scipy.interpolate
import matplotlib.pyplot as plt
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
lambdas = [50, 5.0, 3.0, 2.0, 1.5]
path = 'data/BlockDiag_soft_4.0_0.5_*/{}'
#  path = 'data/BandDiag_soft_1.25_0.2_*/{}'
#  path = 'data/T_rel_*/{}'
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
nodes = np.linspace(0.0, kmax, 40)

# Get generator
generator = np.array(data['generator'])

interp = scipy.interpolate.RectBivariateSpline(data_nodes, data_nodes,
                                               generator)

generator_interp = -1 * interp(nodes, nodes)

for i in range(len(generator_interp)):
    generator_interp[i][i] = 1.0

fig, ax = plt.subplots()
ax.matshow(generator_interp, extent=[0, kmax, kmax, 0], vmax=1, vmin=-1,
            cmap=plt.get_cmap('bwr'))
ax.set_xticks([0, 5, 10])
ax.set_yticks([0, 5, 10])
ax.tick_params(
    axis='x',
    which='both',
    bottom=True,
    top=False,
    labelbottom=True,
    labeltop=False,
)

#  ax.xaxis.set_label_position('top')

plt.xlabel(r"$k'$ (fm$^{-1}$)")
plt.ylabel(r'$k$ (fm$^{-1}$)')
plt.title('Generator Form', x=0.5, y=1.05)

#  plt.gcf().subplots_adjust(left=0.075)
plt.gcf().subplots_adjust(right=1.05)
plt.gcf().subplots_adjust(top=0.85)
plt.gcf().subplots_adjust(bottom=0.22)
plt.gcf().set_size_inches(1.5 * fig_height, 1.6 * fig_height)
plt.savefig('generator.pdf')

