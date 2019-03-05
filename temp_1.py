#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec

from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import Spin, OrbitalType


def rgbline(ax, k, e, red, green, blue, alpha=1.):
    # creation of segments based on
    # http://nbviewer.ipython.org/urls/raw.github.com/dpsanders/matplotlib-examples/master/colorline.ipynb
    pts = np.array([k, e]).T.reshape(-1, 1, 2)
    seg = np.concatenate([pts[:-1], pts[1:]], axis=1)

    nseg = len(k) - 1
    r = [0.5 * (red[i] + red[i + 1]) for i in range(nseg)]
    g = [0.5 * (green[i] + green[i + 1]) for i in range(nseg)]
    b = [0.5 * (blue[i] + blue[i + 1]) for i in range(nseg)]
    a = np.ones(nseg, np.float) * alpha
    lc = LineCollection(seg, colors=list(zip(r, g, b, a)), linewidth=2)
    ax.add_collection(lc)


if __name__ == "__main__":
    # read data
    # ---------

    # kpoints labels
    labels = [r"$L$", r"$\Gamma$", r"$X$", r"$U,K$", r"$\Gamma$"]

    # density of states
    dosrun = Vasprun("./DOS/vasprun.xml")
    spd_dos = dosrun.complete_dos.get_spd_dos()

    # bands
    run = Vasprun("./Bandes/vasprun.xml", parse_projected_eigen=True)
    bands = run.get_band_structure("./Bandes/KPOINTS",
                                   line_mode=True,
                                   efermi=dosrun.efermi)

    # set up matplotlib plot
    # ----------------------

    # general options for plot
    font = {'family': 'serif', 'size': 24}
    plt.rc('font', **font)

    # set up 2 graph with aspec ration 2/1
    # plot 1: bands diagram
    # plot 2: Density of States
    gs = GridSpec(1, 2, width_ratios=[2, 1])
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Bands diagram of copper")
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])  # , sharey=ax1)

    # set ylim for the plot
    # ---------------------
    emin = -10.
    emax = 10.
    ax1.set_ylim(emin, emax)
    ax2.set_ylim(emin, emax)

    # Band Diagram
    # ------------
    name = {}
    tmp_atom = {}.fromkeys(run.atomic_symbols).keys()
    for i in tmp_atom:
        name[i] = ["s", "p", "d"]
    pbands = bands.get_projections_on_elements_and_orbitals(name)