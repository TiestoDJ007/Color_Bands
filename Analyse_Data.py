#!/usr/bin/env python
# -*- coding=utf-8 -*-

import copy
import pickle

from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


# 生成不同原子的Projected_Bands
def Pbands_Separate(i):
    pbands_tmp = copy.deepcopy(pbands)
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for n in pbands[Spin.up][b][k].keys():
                if n != i:
                    del pbands_tmp[Spin.up][b][k][n]
    return pbands_tmp


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
    name = {}
    orbit_atom = sorted(set(vasprun.atomic_symbols), key=vasprun.atomic_symbols.index)
    for i in orbit_atom:
        name[i] = ["s", "p", "d"]
    pbands = bands.get_projections_on_elements_and_orbitals(name)

    # 动态生成相应原子的名称，以及画图所需数据
    pbands_atom = {}
    for i in orbit_atom:
        pbands_atom[i] = Pbands_Separate(i)

    #最后需要手动输出文件，详情请见变量保存

