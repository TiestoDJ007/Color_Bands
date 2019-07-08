#!/usr/bin/env python
# -*- coding=utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from numpy import cos, sin, sqrt, arctan2
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


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

    efermi = vasp_data[0].efermi

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

    Energy_Band_52 = []
    for energy_band in band_data:
        energy_data = energy_band.bands[Spin.up][52]
        Energy_Band_52.extend(energy_data.tolist())
    Energy_Band_52 = np.array(Energy_Band_52) - efermi

    Energy_Band_51 = []
    for energy_band in band_data:
        energy_data = energy_band.bands[Spin.up][51]
        Energy_Band_51.extend(energy_data.tolist())
    Energy_Band_51 = np.array(Energy_Band_51) - efermi

    Band_52 = np.column_stack((polar_Position, Energy_Band_52))
    Band_51 = np.column_stack((polar_Position, Energy_Band_51))

    Fermi_Surface_52 = []
    for num_point in range(len(Band_52)):
        if -0.005 < Band_52[num_point][2] < 0.005:
            Fermi_Surface_52.append(np.array((Band_52[num_point][0], Band_52[num_point][1])))
    Fermi_Surface_52 = np.array(Fermi_Surface_52)

    Fermi_Surface_51 = []
    for num_point in range(len(Band_51)):
        if -0.005 < Band_51[num_point][2] < 0.005:
            Fermi_Surface_51.append(np.array((Band_51[num_point][0], Band_51[num_point][1])))
    Fermi_Surface_51 = np.array(Fermi_Surface_51)

    Sort_Fermi_Surface_52 = Fermi_Surface_52[np.argsort(Fermi_Surface_52[:, 1])]

    Split_Fermi_Surface_52 = np.array_split(Sort_Fermi_Surface_52, 30, axis=0)

    circle_52_in, circle_52_out = [], []
    for num_split in range(len(Split_Fermi_Surface_52)):
        Max_point = np.argmax(Split_Fermi_Surface_52[num_split][:, 0])
        Min_point = np.argmin(Split_Fermi_Surface_52[num_split][:, 0])
        circle_52_out.append(Split_Fermi_Surface_52[num_split][Max_point])
        circle_52_in.append(Split_Fermi_Surface_52[num_split][Min_point])
    circle_52_in = np.array(circle_52_in)
    circle_52_out = np.array(circle_52_out)

    Sort_Fermi_Surface_51 = Fermi_Surface_51[np.argsort(Fermi_Surface_51[:, 1])]

    Split_Fermi_Surface_51 = np.array_split(Sort_Fermi_Surface_51, 30, axis=0)

    circle_51_in, circle_51_out = [], []
    for num_split in range(len(Split_Fermi_Surface_51)):
        Max_point = np.argmax(Split_Fermi_Surface_51[num_split][:, 0])
        Min_point = np.argmin(Split_Fermi_Surface_51[num_split][:, 0])
        circle_51_out.append(Split_Fermi_Surface_51[num_split][Max_point])
        circle_51_in.append(Split_Fermi_Surface_51[num_split][Min_point])
    circle_51_in = np.array(circle_51_in)
    circle_51_out = np.array(circle_51_out)

    plot_data_52_in = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in circle_52_in:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_52_in.extend(rot_data)
    plot_data_52_in = np.array(plot_data_52_in)

    plot_data_52_out = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in circle_52_out:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_52_out.extend(rot_data)
    plot_data_52_out = np.array(plot_data_52_out)

    plot_data_51_in = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in circle_51_in:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_51_in.extend(rot_data)
    plot_data_51_in = np.array(plot_data_51_in)

    plot_data_51_out = []
    for rot_num in range(6):
        rot_data = []
        for cart_coordinate in circle_51_out:
            cart_position = (polar2cart(cart_coordinate))
            rot_data.append(rotation_2D(cart_position, rot_num * np.pi / 3))
        plot_data_51_out.extend(rot_data)
    plot_data_51_out.append(plot_data_51_out[0])
    plot_data_51_out = np.array(plot_data_51_out)

    x_brillouin = [1 / 2, 0, -1 / 2, -1 / 2, 0, 1 / 2, 1 / 2]
    y_brillouin = [sqrt(3) / 6, sqrt(3) / 3, sqrt(3) / 6, -sqrt(3) / 6, -sqrt(3) / 3, -sqrt(3) / 6, sqrt(3) / 6]

    plt.figure(figsize=(8, 6))
    plt.plot(plot_data_52_in[:, 0], plot_data_52_in[:, 1], label=r'$\alpha$')
    plt.plot(plot_data_52_out[:, 0], plot_data_52_out[:, 1], label=r'$\beta$')
    plt.plot(plot_data_51_in[:, 0], plot_data_51_in[:, 1], label=r'$\gamma$')
    plt.plot(plot_data_51_out[:, 0], plot_data_51_out[:, 1], label=r'$\delta$')
    plt.plot([0, 0.5], [0, 0], color='navy')
    plt.plot([0, 0.5], [0, sqrt(3) / 6], color='navy')
    plt.plot(x_brillouin, y_brillouin, color='k')
    plt.text(-0.75, 0.5, 'FS', size=25)
    plt.text(-0.04, -0.06, r'$\Gamma$', size=16)
    plt.text(0.52, -0.06, 'M', size=16)
    plt.text(0.52, sqrt(3) / 6, 'K', size=16)
    plt.xlabel('{}'.format('$k_x$' + '(' + '$\AA^{-1}$' + ')'), size=16)
    plt.ylabel('{}'.format('$k_y$' + '(' + '$\AA^{-1}$' + ')'), size=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.axis("equal")
    plt.legend(loc=0, fontsize=16, mode="expand", frameon=False)
    plt.savefig('{}'.format('/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Picture/FS.png'))
    plt.show()
