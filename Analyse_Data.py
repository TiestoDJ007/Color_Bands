#!/usr/bin/env python
# -*- coding=utf-8 -*-

import copy

import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun

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
    contrib = np.zeros((len(orbit_atom), bands.nb_bands, len(bands.kpoints), 3))
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for atom_name in orbit_atom:
                sc = pbands[Spin.up][b][k][atom_name]["s"] ** 2
                pc = pbands[Spin.up][b][k][atom_name]["p"] ** 2
                dc = pbands[Spin.up][b][k][atom_name]["d"] ** 2
                tot = sc + pc + dc
                if tot != 0.0:
                    contrib[orbit_atom.index(atom_name), b, k, 0] = sc / tot
                    contrib[orbit_atom.index(atom_name), b, k, 1] = pc / tot
                    contrib[orbit_atom.index(atom_name), b, k, 2] = dc / tot


    # 生成不同原子的pdos
    def pbands_atom(i):
        pbands_tmp = copy.deepcopy(pbands)
        for b in range(bands.nb_bands):
            for k in range(len(bands.kpoints)):
                for n in pbands[Spin.up][b][k].keys():
                    if n != i:
                        del pbands_tmp[Spin.up][b][k][n]
        return pbands_tmp


    # 动态生成相应原子的名称
    for i in orbit_atom:
        locals()['pbands_' + i] = pbands_atom(i)
