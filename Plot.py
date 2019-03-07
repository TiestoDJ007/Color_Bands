#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pickle
import sys

import matplotlib.pyplot as plt
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
    bands = pickle.load(open('bands.txt', 'rb'))
    # 开始画图
    labels = [r"$L$", r"$\Gamma$", r"$X$", r"$U,K$", r"$\Gamma$"]
    font = {'family': 'serif', 'size': 24}
    plt.rc('font', **font)
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = plt.plot()
    # 设置Y轴最大值最小值
    # 颜色变化程度
    # 手动输入画图的原子
    contrib = np.zeros((bands.nb_bands, len(bands.kpoints), 3))
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            sc = pbands[b][k]['s'] ** 2
            pc = pbands[b][k]['p'] ** 2
            dc = pbands[b][k]['d'] ** 2
            tot = sc + pc + dc
            if tot != 0.0:
                contrib[b, k, 0] = sc / tot
                contrib[b, k, 1] = pc / tot
                contrib[b, k, 2] = dc / tot


    for b in range(bands.nb_bands):
        rgbline(ax,
                range(len(bands.kpoints)),
                [e - bands.efermi for e in bands.bands[Spin.up][b]],
                contrib[b, :, 0],
                contrib[b, :, 1],
                contrib[b, :, 2])

    fig.set_xlabel("k-points")
    fig.set_ylabel(r"$E - E_f$   /   eV")
    fig.grid()
    fig.hlines(y=0, xmin=0, xmax=len(bands.kpoints), color="k", lw=2)

    # labels
    nlabs = len(labels)
    step = len(bands.kpoints) / (nlabs - 1)
    for i, lab in enumerate(labels):
        ax.vlines(i * step, emin, emax, "k")
    ax.set_xticks([i * step for i in range(nlabs)])
    ax.set_xticklabels(labels)

    ax.set_xlim(0, len(bands.kpoints))

    plt.subplots_adjust(wspace=0)

    # plt.show()
    plt.savefig(sys.argv[0].strip(".py") + ".pdf", format="pdf")
