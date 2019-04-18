#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


def difference(x1, x2, y1, y2):
    if x1 == x2:
        pass
    else:
        x = (x1 + x2) / 2
        y = (y2 - y1) / (x2 - x1)
        return x, y


if __name__ == "__main__":
    vasprun_dirctory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Band/'
    vasprun_file = 'vasprun_a_-2%.xml'
    kpoints_file = 'KPOINTS'
    procar_file = 'PROCAR_a_-2%'
    saving_dictory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Picture/Band/'
    saving_file = '{}'.format(vasprun_file.strip('vasprun_' + '.xml') + '_Band')
    vasprun = Vasprun("{}".format(vasprun_dirctory + vasprun_file))
    bands = vasprun.get_band_structure(
        "{}".format(vasprun_dirctory + kpoints_file),
        line_mode=True, efermi=vasprun.efermi)

    bands_number = 51
    Fermi_Velociy = []
    for i in range(len(bands.kpoints)):
        if i == 179:
            break
        else:
            Fermi_Velociy.append(
                difference(bands.distance[i], bands.distance[i + 1],
                           bands.bands[Spin.up][bands_number][i],
                           bands.bands[Spin.up][bands_number][i + 1]))
