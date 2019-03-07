#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pickle

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


    # 动态生成相应原子的名称，以及画图所需数据
    PBands_Mg = Pbands_Separate('Mg')
    save_variable(PBands_Mg, 'PBands_Mg.txt')
    save_variable(bands,'bands.txt')

    # 最后需要手动输出文件，详情请见变量保存
