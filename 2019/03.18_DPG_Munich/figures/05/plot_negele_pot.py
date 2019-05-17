"""Script to plot Negel potential in coordinate space."""
import math as m

import matplotlib.pyplot as plt
import matplotlib


# pylint: disable=C0103
def v_negele(x, v1=12.0, sig1=0.2, v2=-12.0, sig2=0.8):
    """Calculate value of Negele potential at local coordinate `x`."""
    term1 = v1 / (sig1 * m.sqrt(m.pi)) * m.exp(-1 * x ** 2 / sig1 ** 2)
    term2 = v2 / (sig2 * m.sqrt(m.pi)) * m.exp(-1 * x ** 2 / sig2 ** 2)
    return term1 + term2


# Set matplotlib latex preamble
matplotlib.rcParams["text.latex.preamble"] = [
    r"\usepackage{siunitx}",
    r"\sisetup{detect-all}",
    r"\usepackage{helvet}",
    r"\usepackage{sansmath}",
    r"\sansmath",
]
plt.rc("text", usetex=True)

# Generate data for plot
x_vals = [n * 0.01 for n in range(201)]
v_vals = [v_negele(x) for x in x_vals]

# Create figure
fig, ax = plt.subplots()

# Plot data
ax.plot(x_vals, v_vals)

# Show horizontal line V=0
ax.axhline(0, color="black", lw=0.75)

# Set xlimits for plot
plt.xlim(0, 2)

# Labels
plt.xlabel(r"$x_i - x_j$ (fm)")
plt.ylabel(r"$V_{\rm{Negele}}$ (MeV)")

# Adjust margins
plt.gcf().subplots_adjust(left=0.175)
# plt.gcf().subplots_adjust(right=1.100)
plt.gcf().subplots_adjust(top=0.95)
plt.gcf().subplots_adjust(bottom=0.16)

# Set plot size
plt.gcf().set_size_inches(3.0, 3.0)

# Save as PDF
plt.savefig("negele_potential.pdf")
