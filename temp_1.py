#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


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
    orbit_atom = sorted(set(run.atomic_symbols), key=run.atomic_symbols.index)
    for i in orbit_atom:
        name[i] = ["s", "p", "d"]
    pbands = bands.get_projections_on_elements_and_orbitals(name)

    # compute s, p, d normalized contributions
    contrib = np.zeros((len(orbit_atom), bands.nb_bands, len(bands.kpoints), 3))
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for atom_name in orbit_atom:
                sc = pbands[Spin.up][b][k][atom_name]["s"] ** 2
                pc = pbands[Spin.up][b][k][atom_name]["p"] ** 2
                dc = pbands[Spin.up][b][k][atom_name]["d"] ** 2
                tot = sc + pc + dc
                if tot != 0.0:
                    contrib[orbit_atom.index(atom_name), b, k, 0] = sc / tot
                    contrib[orbit_atom.index(atom_name), b, k, 1] = pc / tot
                    contrib[orbit_atom.index(atom_name), b, k, 2] = dc / tot

    # plot bands using rgb mapping
    rgbline_atom = {}
    for b in range(bands.nb_bands):
        for atom_name in orbit_atom:
            rgbline(ax1,
                    range(len(bands.kpoints)),
                    [e - bands.efermi for e in bands.bands[Spin.up][b]],
                    contrib[orbit_atom.index(atom_name), b, :, 0],
                    contrib[orbit_atom.index(atom_name), b, :, 1],
                    contrib[orbit_atom.index(atom_name), b, :, 2])
            rgbline_atom[atom_name] = ax1

            contrib = np.zeros((len(orbit_atom), bands.nb_bands, len(bands.kpoints), 3))
            for b in range(bands.nb_bands):
                for k in range(len(bands.kpoints)):
                    for atom_name in orbit_atom:
                        sc = pbands[Spin.up][b][k][atom_name]["s"] ** 2
                        pc = pbands[Spin.up][b][k][atom_name]["p"] ** 2
                        dc = pbands[Spin.up][b][k][atom_name]["d"] ** 2
                        tot = sc + pc + dc
                        if tot != 0.0:
                            contrib[orbit_atom.index(atom_name), b, k, 0] = sc / tot
                            contrib[orbit_atom.index(atom_name), b, k, 1] = pc / tot
                            contrib[orbit_atom.index(atom_name), b, k, 2] = dc / tot