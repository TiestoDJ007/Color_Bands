# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
import plotly
import plotly.plotly  as py
import plotly.graph_objs as go
from numpy import cos,sin
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp import Vasprun


def rotation(cart,theta):
    rotation_matrix = np.array([[cos(theta),-sin(theta),0],
                                [sin(theta),cos(theta),0],
                                [0,0,1]])
    cart_re = np.dot(rotation_matrix,cart)
    return cart_re

def refliction(cart,theta):
    refliction_matrix = np.array([[cos(2*theta),sin(2*theta),0],
                                  [sin(2*theta),-cos(2*theta),0],
                                  [0,0,1]])
    re_cart = np.dot(refliction_matrix,cart)
    return re_cart

if __name__ == "__main__":
    #plotly.tools.set_credentials_file(username='TiestoDJ007', api_key='2mw1gohx77')
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
    rec_Position_0 = np.dot(rec_Parametar, rec_BVector)
    #rec_Position_ro=[]
    #for cart in rec_Position:
    #    rec_Position_ro.append(refliction(cart,np.pi/6))
    #rec_Position_ro = np.array(rec_Position_ro)
    Energy_Band_51 = np.concatenate((bands_part1.bands[Spin.up][51], bands_part2.bands[Spin.up][51]),axis=0)
    Energy_Band_53 = np.concatenate((bands_part1.bands[Spin.up][53], bands_part2.bands[Spin.up][53]),axis=0)
    Energy_Band_tot = np.concatenate((Energy_Band_51,Energy_Band_53),axis=0)
    data_0 = np.column_stack((rec_Parametar,Energy_Band_51))
    data_1 = np.column_stack((rec_Parametar, Energy_Band_53))
    data_ref_tmp=[]
    for cart in data_0:
        data_ref_tmp.append(refliction(cart,0))
    data_ref = np.array(data_ref_tmp)
    data = np.concatenate((data_0,data_ref),axis=0)

    data_rot_tmp = []
    for cart_rot in data:
        data_rot_tmp.append(rotation(cart_rot, 1* np.pi / 3))
    data_rot_1 = np.array(data_rot_tmp)
    data_rot_tmp = []
    for cart_rot in data:
        data_rot_tmp.append(rotation(cart_rot, 2* np.pi / 3))
    data_rot_2 = np.array(data_rot_tmp)
    data_rot_tmp = []
    for cart_rot in data:
        data_rot_tmp.append(rotation(cart_rot, 3* np.pi / 3))
    data_rot_3= np.array(data_rot_tmp)
    data_rot_tmp = []
    for cart_rot in data:
        data_rot_tmp.append(rotation(cart_rot, 4* np.pi / 3))
    data_rot_4 = np.array(data_rot_tmp)
    data_rot_tmp = []
    for cart_rot in data:
        data_rot_tmp.append(rotation(cart_rot, 5* np.pi / 3))
    data_rot_5 = np.array(data_rot_tmp)

    data_tot_tmp = np.concatenate((data,data_rot_1,data_rot_2,data_rot_3,data_rot_4,data_rot_5),axis=0)
    data_half_tot = np.concatenate((data_rot_5, data_rot_4), axis=0)
    data_tot = np.round(np.unique(data_tot_tmp,axis=0),decimals=4)

    plot_data = [
        go.Scatter3d(
            x=data_half_tot[:,0],
            y=data_half_tot[:,1],
            z=data_half_tot[:,2],
            mode='markers',
            marker={"size":1,"showscale": True, "color": data_half_tot[:,2]}

    )
    ]

    layout = go.Layout(
        width=800,
        height=700,
        autosize=False,
        title='Volcano dataset',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual'
        )
    )

    fig = dict(data=plot_data, layout=layout)
    plotly.offline.plot(fig,filename='test.html')