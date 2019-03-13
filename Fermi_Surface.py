#!/usr/bin/env python
# -*- coding=utf-8 -*-

import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun

vasprun = Vasprun('C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Fermi_Surface/vasprun.xml')
bands = vasprun.get_band_structure('C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Fermi_Surface/KPOINTS',
                                   efermi=vasprun.efermi,
                                   line_mode=True)
kpoints = np.zeros((len(bands.kpoints), 3))
for i in range(len(bands.kpoints)):
    kpoints[i][0] = bands.kpoints[i].a
    kpoints[i][1] = bands.kpoints[i].b

emin = 0
emax = 0
for i in range(bands.nb_bands):
    for j in range(len(bands.kpoints)):
        energy_temp = bands.bands[Spin.up][i][j] - bands.efermi
        if emin<= energy_temp and energy_temp<= emax:
