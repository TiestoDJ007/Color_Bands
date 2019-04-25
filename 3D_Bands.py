#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin
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
    reciprocal = vasprun.lattice_rec
    #定义基矢
    rec_BVector = reciprocal.matrix[0:2,0:2]
    #定义坐标
    rec_Parametar = np.array(vasprun.actual_kpoints)[:,0:2]
    #实际坐标
    rec_Position = np.dot(rec_Parametar,rec_BVector)
    #选取能量，如band=53和band=55的能量
    Energy_Band_53 = bands.bands[Spin.up][53]
    Energy_Band_51 = bands.bands[Spin.up][51]

    fig = plt.figure(figsize=(16, 10))
    ax = fig.gca(projection='3d')
    X = rec_Position[:,0]
    Y = rec_Position[:,1]
    Z1 = Energy_Band_53
    Z2 = Energy_Band_51
    ax.plot_trisurf(X, Y, Z2, linewidth=0,cmap='winter',edgecolor='none')
    #ax.plot_trisurf(X, Y, Z2, linewidth=0.1,color='b')
    ax.view_init(90, 0)
    plt.show()