#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    # vasprun.xml位置
    vasprun = Vasprun("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/vasprun_0%.xml",
                      parse_projected_eigen=True)
    # 生成独立的band数据
    bands = vasprun.get_band_structure("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/KPOINTS",
                                       line_mode=True, efermi=vasprun.efermi)
    # 读取投影数据
    procar = Procar("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/PROCAR_0%")
    # 原子选择
    Plot_Atom = 'C'
    Atom_symbol = vasprun.atomic_symbols
    dot_size = np.zeros(((3, bands.nb_bands, len(bands.kpoints))))
    for n in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            # 挑选出投影原子的点大小数据
            for atom_nb in range(len(Atom_symbol)):
                if Atom_symbol[atom_nb] == Plot_Atom:
                    dot_size[0][n][k] += procar.data[Spin.up][k][n][atom_nb][3] * 300
                    dot_size[1][n][k] += procar.data[Spin.up][k][n][atom_nb][1] * 300
                    dot_size[2][n][k] += procar.data[Spin.up][k][n][atom_nb][2] * 300
    # 选定能量区间
    energy_min = -1
    energy_max = 1
    # 高对称点设置
    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    labels_position = list()
    font = {'family': 'sans-serif', 'size': 24}
    # 开始画图
    fig, ax1 = plt.subplots(figsize=(8, 5))
    # 设置刻度向内
    ax1.tick_params(direction='in')
    # 设置能量区间
    ax1.set_ylim(energy_min, energy_max)
    # 设置x轴区间
    ax1.set_xlim(bands.distance[0], bands.distance[-1])
    ax1.set_xlabel("k-points")
    ax1.set_ylabel(r"$E - E_f$   /   eV")
    # 寻找高对称点
    for i in range(len(bands.distance)):
        if i == 0:
            labels_position.append(bands.distance[i])
        elif i < len(bands.distance) - 2:
            if bands.distance[i] == bands.distance[i + 1]:
                labels_position.append(bands.distance[i])
                # 设置垂直线
                ax1.vlines(bands.distance[i], energy_min, energy_max, colors='gray', linestyles='dashed')
        elif i == len(bands.distance) - 1:
            labels_position.append(bands.distance[i])
    # 展示高对称点
    ax1.set_xticks(labels_position)
    ax1.set_xticklabels(labels)
    ax1.xaxis.set_major_locator
    # 图像标题
    ax1.set_title('C Orbital p Projected Bands')
    # 画散点图
    for n in range(bands.nb_bands):
        band_px = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[0][n], color='r', marker='.')
        band_py = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[1][n], color='b', marker='.')
        band_pz = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[2][n], color='g', marker='.')
    # 设置平行线
    ax1.hlines(0, labels_position[0], labels_position[-1])
    #plt.savefig('/mnt/c/Users/jackx/Desktop/test_z.png', dpi=300)
    plt.show()
