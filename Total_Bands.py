#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt

from pymatgen.io.vasp.outputs import Vasprun

if __name__ == "__main__":
    vasprun_dirctory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Band/'
    vasprun_file = 'vasprun_a_-2%.xml'
    kpoints_file = 'KPOINTS'
    procar_file = 'PROCAR_a_-2%'
    saving_dictory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Picture/Band/'
    saving_file = '{}'.format(vasprun_file.strip('vasprun_' + '.xml') + '_Band' )
    vasprun = Vasprun("{}".format(vasprun_dirctory + vasprun_file))
    band = vasprun.get_band_structure("{}".format(vasprun_dirctory+kpoints_file),
                                       line_mode=True, efermi=vasprun.efermi)

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