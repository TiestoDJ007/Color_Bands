#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pymatgen.io.vasp.outputs import Vasprun

vasprun = Vasprun('/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/DOS/vasprun_0%.xml')
PDOS = vasprun.pdos
TDOS = vasprun.tdos.densities
ENERGY_POINTS = vasprun.tdos.energies

