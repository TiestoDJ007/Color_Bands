import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin  # 引入Spin函数，使之能被索引
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    vasprun = Vasprun("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/vasprun_0%.xml",
                      parse_projected_eigen=True)
    bands = vasprun.get_band_structure("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/KPOINTS",
                                       line_mode=True, efermi=vasprun.efermi)
    procar = Procar("/mnt/c/Users/jackx/OneDrive/Calculation_Data/Mg2C_Graphene/Band/PROCAR_0%")
    # 9-22是C原子
    Plot_Atom = 'C'
    Atom_symbol = vasprun.atomic_symbols
    dot_size = np.zeros(((3, bands.nb_bands, len(bands.kpoints))))
    for n in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for atom_nb in range(len(Atom_symbol)):
                if Atom_symbol[atom_nb] == Plot_Atom:
                    dot_size[0][n][k] += procar.data[Spin.up][k][n][atom_nb][2] * 1000
                    dot_size[1][n][k] += procar.data[Spin.up][k][n][atom_nb][1] * 1000
                    dot_size[2][n][k] += procar.data[Spin.up][k][n][atom_nb][3] * 1000

    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    font = {'family': 'sans-serif', 'size': 24}
    fig, ax1 = plt.subplots()
    nlabs = len(labels)
    step = len(bands.kpoints) / (nlabs - 1)
    ax1.set_ylim(-1, 1)
    ax1.set_xlabel("k-points")
    ax1.set_ylabel(r"$E - E_f$   /   eV")
    ax1.grid()
    ax1.set_title('C Orbital p Projected Bands')
    for n in range(bands.nb_bands):
        band_px = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[0][n], color='r',
                              marker='.')
        band_py = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[1][n], color='b',
                              marker='.')
        band_pz = ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[2][n], color='g',
                              marker='.')
    plt.show()
