import numpy as np
import matplotlib.pyplot as plt

vs = np.linspace(0.0, 1.0, 129)
ps = -0.5 * np.log(1 - vs**2)

fig, ax = plt.subplots()
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlabel("Slope / critical slope")
ax.set_ylabel("Free power")
ax.plot(vs, ps)
fig.savefig("hillslope-primal.png", dpi=300)


qs = np.linspace(0.0, 1.0, 129)
ps = np.sqrt(4 * qs**2 + 1) - 1 - np.log(2 / (np.sqrt(4 * qs**2 + 1) + 1))

fig, ax = plt.subplots()
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlabel("Flux")
ax.set_ylabel("Free power")
ax.plot(qs, ps)
fig.savefig("hillslope-dual.png", dpi=300)
