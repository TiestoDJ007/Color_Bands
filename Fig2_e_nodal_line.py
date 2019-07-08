# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from numpy import cos, sin, sqrt, arctan2
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp import Vasprun


def rotation_2D(cart, theta):
    rotation_matrix = np.array([[cos(theta), -sin(theta)],
                                [sin(theta), cos(theta)]])
    return np.matmul(rotation_matrix, cart)


def cart2polar(cart):
    radius = np.linalg.norm(cart, ord=2)
    theta = arctan2(cart[1], cart[0])
    return np.array([radius, theta])


def polar2cart(cart):
    x_coordinate = cart[0] * cos(cart[1])
    y_coordinate = cart[0] * sin(cart[1])
    return np.array([x_coordinate, y_coordinate])


if __name__ == "__main__":
    split_number = 24
    root = "/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Nodal_Line/"

    vasp_data = []
    band_data = []
    for num_data in range(split_number):
        vasprun_file_name = 'vasprun_split_part_{}.xml'.format(num_data)
        kpoints_file_name = 'KPOINTS_split_part_{}.xml'.format(num_data)
        vasp_data.append(Vasprun("{}".format(root + vasprun_file_name)))
        band_data.append(vasp_data[num_data].get_band_structure(
            "{}".format(root + kpoints_file_name),
            efermi=vasp_data[num_data].efermi,
            line_mode=False))

    rec_coordinate = []
    for num_rec in range(len(vasp_data)):
        rec_coordinate.extend(vasp_data[num_rec].actual_kpoints)
    rec_coordinate = np.array(rec_coordinate)[:, 0:2]

    shearing_matrix = np.array([[1, 1 / 2],
                                [0, sqrt(3) / 2]])
    rec_Position_shearing = []
    for rec_cart in rec_coordinate:
        rec_Position_shearing.append(np.matmul(shearing_matrix, rec_cart))
    rec_Position = np.array(rec_Position_shearing)

    polar_Position = []
    for cart_rec in rec_Position:
        polar_cart = cart2polar(cart_rec)
        polar_Position.append(polar_cart)
    polar_Position = np.array(polar_Position)

    Energy_Band_51 = []
    for energy_band in band_data:
        energy_data = energy_band.bands[Spin.up][51]
        Energy_Band_51.extend(energy_data.tolist())
    Energy_Band_51 = np.array(Energy_Band_51)
    Energy_Band_53 = []
    for energy_band in band_data:
        energy_data = energy_band.bands[Spin.up][53]
        Energy_Band_53.extend(energy_data.tolist())
    Energy_Band_53 = np.array(Energy_Band_53)

    data_51_sort = np.column_stack((polar_Position, Energy_Band_51))
    data_53_sort = np.column_stack((polar_Position, Energy_Band_53))

    data_51 = data_51_sort[np.argsort(data_51_sort[:, 1])]
    data_53 = data_53_sort[np.argsort(data_53_sort[:, 1])]

    #设置扇形大小，分辨率
    data_51_split = np.array_split(data_51, 80, axis=0)
    data_53_split = np.array_split(data_53, 80, axis=0)

    # 旋转一个无限小的角度，旋转出的扇形近似为一条直线，选取这条直线上最大或者最小的数值，即是能带最大或最小的值
    plot_data_polar_51 = []
    for num_split in range(len(data_51_split)):
        max_point = np.argmax(data_51_split[num_split][:, 2])
        plot_data_polar_51.append(data_51_split[num_split][max_point][0:2])
    plot_data_polar_51 = np.array(plot_data_polar_51)
    plot_data_polar_53 = []
    for num_split in range(len(data_53_split)):
        max_point = np.argmin(data_53_split[num_split][:, 2])
        plot_data_polar_53.append(data_53_split[num_split][max_point][0:2])
    plot_data_polar_53 = np.array(plot_data_polar_53)

    plot_data_cart_51 = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in plot_data_polar_51:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_cart_51.extend(rot_data)
    plot_data_cart_51 = np.array(plot_data_cart_51)
    plot_data_cart_53 = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in plot_data_polar_53:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_cart_53.extend(rot_data)
    plot_data_cart_53 = np.array(plot_data_cart_53)

    plt.figure(figsize=(8, 6))
    x_51 = plot_data_cart_51[:, 0]
    y_51 = plot_data_cart_51[:, 1]
    x_53 = plot_data_cart_53[:, 0]
    y_53 = plot_data_cart_53[:, 1]
    x_brillouin = [1 / 2, 0, -1 / 2, -1 / 2, 0, 1 / 2, 1 / 2]
    y_brillouin = [sqrt(3) / 6, sqrt(3) / 3, sqrt(3) / 6, -sqrt(3) / 6, -sqrt(3) / 3, -sqrt(3) / 6, sqrt(3) / 6]
    plt.axis("equal")
    plt.xlim((-0.6, 0.6))
    plt.ylim((-0.6, 0.6))
    plt.xlabel('{}'.format('$k_x$'+'('+'$\AA^{-1}$'+')'),size=16)
    plt.ylabel('{}'.format('$k_y$' + '(' + '$\AA^{-1}$' + ')'), size=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.text(-0.75,0.5,'NL',size=25)
    plt.text( -0.04, -0.06, r'$\Gamma$', size=16)
    plt.text(0.52, -0.06, 'M', size=16)
    plt.text(0.52, sqrt(3) / 6, 'K', size=16)
    plt.plot([0,0.5],[0,0],color='g')
    plt.plot([0,0.5],[0,sqrt(3)/6],color='g')
    plt.plot(x_51, y_51, color='b',label='NL1')
    plt.plot(x_53, y_53, color='r',label='NL2')
    plt.legend(loc=0,fontsize=16,edgecolor='w' )
    plt.plot(x_brillouin, y_brillouin, color='k')

    plt.show()
