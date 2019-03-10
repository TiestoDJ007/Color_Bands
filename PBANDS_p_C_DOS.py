import sys
from copy import deepcopy

import matplotlib.pyplot as plt
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
    dosrun = Vasprun("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/DOS/vasprun.xml")
    # 将bands.projections转化成n维数组
    tmp_pbands = list(bands.projections.values())
    pbands_ndarray = deepcopy(tmp_pbands[0])
    # 分别投影到原子和轨道
    pbands_py_C = np.sum(deepcopy(pbands_ndarray[:, :, 1, 8:30]), axis=2)
    pbands_px_C = np.sum(deepcopy(pbands_ndarray[:, :, 2, 8:30]), axis=2)
    pbands_pz_C = np.sum(deepcopy(pbands_ndarray[:, :, 3, 8:30]), axis=2)

    # 输出投影原子，轨道的贡献率
    contrib_p_C = np.zeros((bands.nb_bands, len(bands.kpoints), 3))
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            px = pbands_px_C[b][k] ** 2
            py = pbands_py_C[b][k] ** 2
            pz = pbands_pz_C[b][k] ** 2
            tot_p = px + py + pz
            if tot_p != 0.0:
                contrib_p_C[b, k, 0] = px / tot_p
                contrib_p_C[b, k, 1] = py / tot_p
                contrib_p_C[b, k, 2] = pz / tot_p

    # 设置绘图参数
    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    font = {'family': 'sans-serif', 'size': 24}
    fig, ax1 = plt.subplots()
    ax1.set_ylim(-1,1)
    for b in range(bands.nb_bands):
        rgbline(ax1,
                range(len(bands.kpoints)),
                [e - bands.efermi for e in bands.bands[Spin.up][b]],
                contrib_p_C[b, :, 0],
                contrib_p_C[b, :, 1],
                contrib_p_C[b, :, 2])
    ax1.set_xlabel("k-points")
    ax1.set_ylabel(r"$E - E_f$   /   eV")
    ax1.grid()
    ax1.hlines(y=0, xmin=0, xmax=len(bands.kpoints), color="k", lw=2)
    nlabs = len(labels)
    step = len(bands.kpoints) / (nlabs - 1)
    for i, lab in enumerate(labels):
        ax1.vlines(i * step, -1, 1, "k")
    ax1.set_xticks([i * step for i in range(nlabs)])
    ax1.set_xticklabels(labels)
    ax1.set_xlim(0, len(bands.kpoints))
    plt.show()
    plt.savefig(sys.argv[0].strip(".py") + ".png", format="png")