#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pickle
import numpy as np
from collections import defaultdict
from copy import deepcopy
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


# 变量保存
def save_variable(Vars, filename):
    f = open(filename, 'wb')
    pickle.dump(Vars, f)
    f.close()
    return filename


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
    # Only Bands
    vasprun = Vasprun("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/vasprun.xml",
                      parse_projected_eigen=True)
    bands = vasprun.get_band_structure("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/KPOINTS",
                                       line_mode=True,
                                       efermi=vasprun.efermi)
    # 将bands.projections转化成n维数组
    tmp_pbands = list(bands.projections.values())
    pbands_ndarray = deepcopy(tmp_pbands[0])
    # 分别投影到原子和轨道
    pbands_s_Mg = np.sum(deepcopy(pbands_ndarray[:, :, 0, 0:8]), axis=2)
    pbands_p_Mg = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 1:4, 0:8]), axis=2), axis=2)
    pbands_d_Mg = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 4:9, 0:8]), axis=2), axis=2)
    pbands_s_C = np.sum(deepcopy(pbands_ndarray[:, :, 0, 8:30]), axis=2)
    pbands_p_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 1:4, 8:30]), axis=2), axis=2)
    pbands_d_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 4:9, 8:30]), axis=2), axis=2)
    total = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, :, :]), axis=2), axis=2)

    # 输出投影原子，轨道的贡献率
    contrib_Origin = np.zeros((bands.nb_bands, len(bands.kpoints), 3))
    contrib_Mg = deepcopy(contrib_Origin)
    contrib_Mg[:, :, 0] = (pbands_s_Mg ** 2) / total
    contrib_Mg[:, :, 1] = (pbands_p_Mg ** 2) / total
    contrib_Mg[:, :, 2] = (pbands_d_Mg ** 2) / total
    contrib_C = deepcopy(contrib_Origin)
    contrib_Mg[:, :, 0] = (pbands_s_Mg ** 2) / total
    contrib_Mg[:, :, 1] = (pbands_p_Mg ** 2) / total
    contrib_Mg[:, :, 2] = (pbands_d_Mg ** 2) / total

    # 绘图

