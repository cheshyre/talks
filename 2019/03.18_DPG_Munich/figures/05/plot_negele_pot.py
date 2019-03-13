import matplotlib.pyplot as plt
import matplotlib
import math as m


def v_negele(x, v1=12.0, sig1=0.2, v2=-12.0, sig2=0.8):
    return v1 / (sig1 * m.sqrt(m.pi)) * m.exp(-1 * x**2 / sig1**2) \
        + v2 / (sig2 * m.sqrt(m.pi)) * m.exp(-1 * x**2 / sig2**2)

x_vals = [n * 0.01 for n in range(201)]
v_vals = [v_negele(x) for x in x_vals]

matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{siunitx}',
    r'\sisetup{detect-all}',
    r'\usepackage{helvet}',
    r'\usepackage{sansmath}',
    r'\sansmath',
]
plt.rc('text', usetex=True)

fig, ax = plt.subplots()

ax.plot(x_vals, v_vals)
ax.axhline(0, color='black', lw=0.75)
plt.xlim(0, 2)

plt.xlabel(r'$x_i - x_j$ (fm)')
plt.ylabel(r'$V_{negele}$ (MeV)')

plt.gcf().subplots_adjust(left=0.175)
#plt.gcf().subplots_adjust(right=1.100)
plt.gcf().subplots_adjust(top=0.95)
plt.gcf().subplots_adjust(bottom=0.16)

plt.gcf().set_size_inches(3.0, 3.0)

plt.savefig('negele_potential.pdf')
