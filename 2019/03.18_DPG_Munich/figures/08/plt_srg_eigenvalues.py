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
#  plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#  plt.rc('font', family='sans-serif')
fig_height = 1.3


#  path = 'data/T_rel*/{}'
path = './fig_data/{}'

file = glob.glob(path.format('t_rel*eigen*.json'))[0]

with open(file) as f:
    data = json.load(f)

lambdas = [float(key) for key in data]
vals = [data[key]['ho3'] for key in data]

fig1, ax1 = plt.subplots()

ax1.plot(lambdas, vals, 'r.', label=r'$T_{rel}$')
ax1.plot(lambdas, vals, 'r-')

file = glob.glob(path.format('BlD*eigen*.json'))[0]

with open(file) as f:
    data = json.load(f)

lambdas = [float(key) for key in data]
vals = [data[key]['ho3'] for key in data]


ax1.plot(lambdas, vals, 'b.', label=r'$Block$')
ax1.plot(lambdas, vals, 'b-')

file = glob.glob(path.format('BaD*eigen*.json'))[0]

with open(file) as f:
    data = json.load(f)

lambdas = [float(key) for key in data]
vals = [data[key]['ho3'] for key in data]


ax1.plot(lambdas, vals, 'm.', label=r'$Block$')
ax1.plot(lambdas, vals, 'm-')


ax1.set_xscale('log')
ax1.set_xticks([1, 2, 5, 10, 20, 50])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

#  plt.title('\"Triton\" Eigenvalue Running')
plt.xlabel(r'$\lambda$')
plt.ylabel(r'$E_3$ (MeV)')
plt.ylim(-3.0, -2.5)
plt.legend(loc='lower right')
#  plt.ylabel('E_3')

#  plt.gcf().set_size_inches(4.4, 3.8)
plt.gcf().subplots_adjust(left=0.30)
plt.gcf().subplots_adjust(right=0.99)
plt.gcf().subplots_adjust(top=0.99)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().set_size_inches(1.7 * fig_height, 1.2 * fig_height)
plt.savefig('eigenvalues.pdf')
