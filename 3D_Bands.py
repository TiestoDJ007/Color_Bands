#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pymatgen.io.vasp.outputs import Vasprun

if __name__ == "__main__":
    vasprun_dirctory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Fermi_Surface/'
    vasprun_file = 'vasprun.xml'
    kpoints_file = 'KPOINTS'
    saving_dictory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Picture/Fermi_Surface/'
    vasprun = Vasprun("{}".format(vasprun_dirctory + vasprun_file))
    bands = vasprun.get_band_structure(
        "{}".format(vasprun_dirctory + kpoints_file), efermi=vasprun.efermi)


##直接拿到空间矢量画出图片