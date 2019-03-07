#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pickle
from copy import deepcopy

import numpy as np
from pymatgen.io.vasp.outputs import Vasprun


# 变量保存
def save_variable(Vars, filename):
    f = open(filename, 'wb')
    pickle.dump(Vars, f)
    f.close()
    return filename


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
    pbands_s_Mg = np.sum(deepcopy(pbands_ndarray[:, :, 0, 0:8]), axis=3)
    pbands_p_Mg = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 1:4, 0:8]), axis=2), axis=3)
    pbands_d_Mg = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 4:9, 0:8]), axis=2), axis=3)
    pbands_s_C = np.sum(deepcopy(pbands_ndarray[:, :, 0, 8:30]), axis=2)
    pbands_p_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 1:4, 8:30]), axis=2), axis=3)
    pbands_d_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 4:9, 8:30]), axis=2), axis=3)

    # 最后需要手动输出文件，详情请见变量保存
