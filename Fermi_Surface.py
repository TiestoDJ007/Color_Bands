#!/usr/bin/env python
# -*- coding=utf-8 -*-

from math import sqrt

import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun

vasprun = Vasprun('C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Fermi_Surface/vasprun.xml')
bands = vasprun.get_band_structure('C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Fermi_Surface/KPOINTS',
                                   efermi=vasprun.efermi,
                                   line_mode=True)
position = np.zeros(shape=(len(bands.kpoints), 2))
position_original = np.zeros(shape=(len(bands.kpoints), 2, 1))
Tr_Matrix = np.array([[1., -sqrt(3) / 3], [0, 2 * sqrt(3) / 3]])
for i in range(len(bands.kpoints)):
    position_original[i][0] = bands.kpoints[i].a
    position_original[i][1] = bands.kpoints[i].b
    temp_0 = np.dot(Tr_Matrix, position_original[i])
    position[i] = temp_0.T

emin = -0.01
emax = 0.01
energy = np.zeros(shape=(len(bands.kpoints)))
for i in range(len(bands.kpoints)):
    for nb in range(bands.nb_bands):
        energy_temp = bands.bands[Spin.up][nb][i] - bands.efermi
        if emin <= energy_temp and emax >= energy_temp:
            energy[i] = 1.
            break
        else:
            energy[i] = 0.

delet_list = []
for i in range(len(bands.kpoints)):
    if energy[i] == 0:
        delet_list.append(i)

position = np.delete(position, delet_list, axis=0)

out_file = open('Fermi_Surface.dat', 'w')
for i in range(position.shape[0]):
    out_file.write("{0:6f} {1:6f} \n".format(position[i][0],
                                             position[i][1]))
out_file.close()
