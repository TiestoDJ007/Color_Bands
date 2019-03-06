#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pickle

import numpy as np
from matplotlib.collections import LineCollection


def rgbline(ax, k, e, red, green, blue, alpha=1.):
    # creation of segments based on
    # http://nbviewer.ipython.org/urls/raw.github.com/dpsanders/matplotlib-examples/master/colorline.ipynb
    pts = np.array([k, e]).T.reshape(-1, 1, 2)
    seg = np.concatenate([pts[:-1], pts[1:]], axis=1)

    nseg = len(k) - 1
    r = [0.5 * (red[i] + red[i + 1]) for i in range(nseg)]
    g = [0.5 * (green[i] + green[i + 1]) for i in range(nseg)]
    b = [0.5 * (blue[i] + blue[i + 1]) for i in range(nseg)]
    a = np.ones(nseg, np.float) * alpha
    lc = LineCollection(seg, colors=list(zip(r, g, b, a)), linewidth=2)
    ax.add_collection(lc)


if __name__ == "__main__":
    # 读取数据,需手动输入数据名称
    pbands = pickle.load(open('PBands_Mg.txt', 'rb'))
    # 开始画图
    labels = [r"$L$", r"$\Gamma$", r"$X$", r"$U,K$", r"$\Gamma$"]
    # 颜色变化程度
    atom_name = 'Mg'  # 手动输入画图的原子
    contrib = np.zeros((bands.nb_bands, len(bands.kpoints), 3))
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            sc = pbands[Spin.up][b][k][atom_name]["s"] ** 2
            pc = pbands[Spin.up][b][k][atom_name]["p"] ** 2
            dc = pbands[Spin.up][b][k][atom_name]["d"] ** 2
            tot = sc + pc + dc
            if tot != 0.0:
                contrib[atom_name, b, k, 0] = sc / tot
                contrib[atom_name, b, k, 1] = pc / tot
                contrib[atom_name, b, k, 2] = dc / tot
