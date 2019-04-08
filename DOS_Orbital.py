#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from pymatgen.electronic_structure.core import Orbital, Spin
from pymatgen.io.vasp.outputs import Vasprun

EMIN = -2
EMAX = 2
vasprun = Vasprun('/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/DOS/vasprun_a_-2%.xml')
Fermi_Energy = vasprun.efermi
Projected_DOS = vasprun.pdos
Energy_Points = np.zeros(len(vasprun.tdos.energies))
for i in range(len(vasprun.tdos.energies)):
    Energy_Points[i] = vasprun.tdos.energies[i] - Fermi_Energy

plot_atom = 'C'
atom_symbol = vasprun.atomic_symbols

plot_data = np.zeros((4, len(Energy_Points)))
for i in range(len(Energy_Points)):
    for atom_nb in range(len(atom_symbol)):
        if plot_atom == atom_symbol[atom_nb]:
            plot_data[0][i] += Projected_DOS[atom_nb][Orbital.s][Spin.up][i]
            plot_data[1][i] += Projected_DOS[atom_nb][Orbital.px][Spin.up][i] + \
                               Projected_DOS[atom_nb][Orbital.py][Spin.up][i] + \
                               Projected_DOS[atom_nb][Orbital.pz][Spin.up][i]
            plot_data[2][i] += Projected_DOS[atom_nb][Orbital.dxy][Spin.up][i] + Projected_DOS[atom_nb][Orbital.dyz][Spin.up][i] + \
                               Projected_DOS[atom_nb][Orbital.dz2][Spin.up][i] + Projected_DOS[atom_nb][Orbital.dxz][Spin.up][i] + \
                               Projected_DOS[atom_nb][Orbital.dx2][Spin.up][i]
#    plot_data[3][i] = TDOS[Spin.up][i]


xmajorLocator   = MultipleLocator(0.8) #将x主刻度标签设置为20的倍数
fig, ax1 = plt.subplots()
font = {'family': 'sans-serif', 'size': 24}
ax1.set_title('Density of States')
ax1.set_xlim(EMIN, EMAX)
ax1.set_ylim(0, max(plot_data[1]) * 1.2)
ax1.tick_params(direction='in')
ax1.plot(Energy_Points, plot_data[0], color='r',label="C Orbit s")
ax1.plot(Energy_Points, plot_data[1], color='g',label="C Orbit p")
ax1.plot(Energy_Points, plot_data[2], color='b',label="C Orbit d")
#ax1.plot(Energy_Points, plot_data[3], color='k',label="totel")
ax1.xaxis.set_major_locator(xmajorLocator)
plt.legend()
plt.show()
