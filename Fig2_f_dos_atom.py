#!/usr/bin/env python
# -*- coding=utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin, Orbital
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    # 原子选择
    atom_carbon = 'C'
    atom_magnesium = 'Mg'
    vasprun_dirctory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Bands_Dos/Strain_0%/'
    vasprun_file = 'vasprun.xml'
    kpoints_file = 'KPOINTS'
    saving_dictory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Picture/'
    vasprun = Vasprun('{}'.format(vasprun_dirctory + vasprun_file), parse_projected_eigen=True)
    atom_symbols = vasprun.atomic_symbols
    list_carbon, list_magnesium = [], []
    for symbol_number in range(len(atom_symbols)):
        if atom_symbols[symbol_number] == atom_carbon:
            list_carbon.append(symbol_number)
        else:
            list_magnesium.append(symbol_number)
    tdos_data = vasprun.tdos.densities[Spin.up]
    tdos_data[0] = 0
    dos_carbon_p, dos_magnesium_d = [], []
    for nb_dos_carbon_p in list_carbon:
        dos_carbon_p.append(vasprun.pdos[nb_dos_carbon_p][Orbital.s][Spin.up] +
                            vasprun.pdos[nb_dos_carbon_p][Orbital.py][Spin.up] +
                            vasprun.pdos[nb_dos_carbon_p][Orbital.px][Spin.up] +
                            vasprun.pdos[nb_dos_carbon_p][Orbital.pz][Spin.up])
    dos_carbon_p = np.array(dos_carbon_p)
    for nb_dos_magnesium_d in list_magnesium:
        dos_magnesium_d.append(vasprun.pdos[nb_dos_magnesium_d][Orbital.s][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.py][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.px][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.pz][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.dx2][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.dxy][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.dxz][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.dyz][Spin.up] +
                               vasprun.pdos[nb_dos_magnesium_d][Orbital.dz2][Spin.up])
    dos_magnesium_d = np.array(dos_magnesium_d)

    plot_carbon_data = np.sum(dos_carbon_p, axis=0)
    plot_carbon_data[0] = 0
    plot_magnesium_data = np.sum(dos_magnesium_d, axis=0)
    plot_magnesium_data[0] = 0
    plot_tdos_data = tdos_data
    plot_xaxis_data = vasprun.complete_dos.energies

    fig = plt.figure()
    plt.plot(plot_xaxis_data - vasprun.efermi, plot_tdos_data, color='k', label='total dos')
    plt.plot(plot_xaxis_data - vasprun.efermi, plot_carbon_data, color='b', label='C p orbital')
    plt.plot(plot_xaxis_data - vasprun.efermi, plot_magnesium_data, color='r', label='Mg d orbital')
    plt.legend()
    plt.xlabel(r"$E - E_f$ / eV")
    plt.ylabel('Density of States')
    #   plt.xlim(-2, 2)
    plt.ylim(0, 12)
    plt.show()
