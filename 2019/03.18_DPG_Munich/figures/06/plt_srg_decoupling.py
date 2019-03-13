import json
import matplotlib.pyplot as plt
import matplotlib
import glob
import numpy as np


matplotlib.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]
plt.rc('text', usetex=True)
#  path = 'data/T_rel*/{}'
path = './fig_data/{}'

fig_height = 1.3

file = glob.glob(path.format('*decoupling.json'))[0]

with open(file) as f:
    data = json.load(f)

lambdas = [float(key) for key in data]
vals = [data[key]['ho'] for key in data]

fig1, ax1 = plt.subplots()

ax1.plot(lambdas, vals, 'r.')
#  ax1.plot(lambdas, vals, 'r-')

ax1.set_xscale('log')
ax1.set_xticks([1, 2, 5, 10, 20, 50])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylim((0, 34))

plt.xlabel(r'$\lambda$')
plt.ylabel(r'$N_{max}$')
plt.gcf().subplots_adjust(left=0.21)
plt.gcf().subplots_adjust(right=0.99)
plt.gcf().subplots_adjust(top=0.99)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().set_size_inches(1.7 * fig_height, 1.2 * fig_height)
plt.savefig('decoupling.pdf')
