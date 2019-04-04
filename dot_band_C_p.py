import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin  # 引入Spin函数，使之能被索引
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    vasprun = Vasprun("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/vasprun_0%.xml",
                      parse_projected_eigen=True)
    bands = vasprun.get_band_structure("/mnt/c/Users/A/OneDrive/Calculation_Data/Mg2C_Graphene/Band/KPOINTS",
                                       line_mode=True, efermi=vasprun.efermi)
    procar = Procar("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/PROCAR_0%")
    #9-22是C原子
    C_Number = 22
    dot_size = np.zeros((( bands.nb_bands, len(bands.kpoints), 3)))
    for n in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for atom in range(C_Number):
                dot_size[n][k][0]=vasprun[]
                dot_size[n][k][0]=vasprun[]
                dot_size[n][k][0]=vasprun[]

    #dot_data = np.zeros(((3,bands.nb_bands,len(bands.kpoints))))
    #for n in range(bands.nb_bands):
    #    for k in range(len(bands.kpoints)):
    #        dot_data[0][b][k]=bands.bands[Spin.up][n][k]
    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    font = {'family': 'sans-serif', 'size': 24}
    fig, ax1 = plt.subplots()
    nlabs = len(labels)
    step = len(bands.kpoints) / (nlabs - 1)
    ax1.set_ylim(-1,1)
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
    ax1.set_title('C Orbital p Projected Bands')
    for i in range(len(bands.kpoints)):
        band_px = ax1.scatter(bands.kpoints[i],dot_size)

