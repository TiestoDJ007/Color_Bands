# -*- coding: utf-8 -*-
# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp import Vasprun

if __name__ == "__main__":
    root = "/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Nodal_Line/"
    data_part1 = Vasprun("{}".format(root + "NL1/vasprun_part1.xml"))
    data_part2 = Vasprun("{}".format(root + "NL1/vasprun_part2.xml"))
    bands_part1 = data_part1.get_band_structure(
        "{}".format(root + 'NL1/KPOINTS_part1'),
        efermi=data_part1.efermi,
        line_mode=False)
    bands_part2 = data_part2.get_band_structure(
        "{}".format(root + 'NL1/KPOINTS_part2'),
        efermi=data_part2.efermi,
        line_mode=False)
    reciprocal = data_part1.lattice_rec
    rec_BVector = reciprocal.matrix[0:2, 0:2]
    rec_Parametar = np.concatenate((np.array(data_part1.actual_kpoints)[:, 0:2],
                                    np.array(data_part2.actual_kpoints)[:, 0:2]),
                                   axis=0)
    rec_Position = np.dot(rec_Parametar, rec_BVector)
    Energy_Band_51 = np.concatenate((bands_part1.bands[Spin.up][51], bands_part2.bands[Spin.up][51]),axis=0)
    Energy_Band_53 = np.concatenate((bands_part1.bands[Spin.up][53], bands_part2.bands[Spin.up][53]),axis=0)

    fig = plt.figure(figsize=(16, 10))
    ax = fig.gca(projection='3d')
    X = rec_Position[:,0]
    Y = rec_Position[:,1]
    Z51 = Energy_Band_51
    Z53 = Energy_Band_53
    ax.plot_trisurf(X, Y, Z51, linewidth=0,cmap='hot',edgecolor='none')
    ax.plot_trisurf(X, Y, Z53, linewidth=0, cmap='hot', edgecolor='none')
    #ax.plot_trisurf(X, Y, Z2, linewidth=0.1,color='b')
    ax.view_init(60, 20)
    plt.show()
