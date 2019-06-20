#!/usr/bin/env python
# -*- coding=utf-8 -*-

import numpy as np
from pymatgen.electronic_structure.core import Orbital, Spin
from pymatgen.io.vasp.outputs import Vasprun

vasprun = Vasprun('/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/DOS/vasprun_a_-2%.xml')
projected_dos = vasprun.pdos
total_dos = vasprun.tdos.get_densities(Spin.up)
ENERGY_POINTS = vasprun.tdos.energies

plot_atom = list(vasprun.final_structure.symbol_set)
atom_symbol = vasprun.atomic_symbols
plot_data = np.zeros((3, len(ENERGY_POINTS)))
for npa in range(len(plot_atom)):
    for nas in range(len(atom_symbol)):
        for i in range(len(ENERGY_POINTS)):
            if plot_atom[npa] == atom_symbol[nas]:
                plot_data[npa][i] += projected_dos[nas][Orbital.s][Spin.up][i] + \
                                     projected_dos[nas][Orbital.py][Spin.up][i] + \
                                     projected_dos[nas][Orbital.pz][Spin.up][i] + \
                                     projected_dos[nas][Orbital.px][Spin.up][i] + \
                                     projected_dos[nas][Orbital.dx2][Spin.up][i] + \
                                     projected_dos[nas][Orbital.dxy][Spin.up][i] + \
                                     projected_dos[nas][Orbital.dxz][Spin.up][i] + \
                                     projected_dos[nas][Orbital.dyz][Spin.up][i] + \
                                     projected_dos[nas][Orbital.dz2][Spin.up][i]
            plot_data[2][i] = total_dos[i]
