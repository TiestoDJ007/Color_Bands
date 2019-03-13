import numpy as np
from pymatgen.electronic_structure.core import Spin  # 引入Spin函数，使之能被索引
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    vasprun = Vasprun("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/vasprun.xml",
                      parse_projected_eigen=True)
    bands = vasprun.get_band_structure("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/KPOINTS",
                                       line_mode=True, efermi=vasprun.efermi)
    procar = Procar("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/PROCAR")

    dot_size = np.zeros((((20,bands.nb_bands,len(bands.kpoints),3))))
    for n in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            for j in range(20,30,1):
                dot_size[j-20][n][k][0]=procar.data[Spin.up][k][n][j][2]
                dot_size[j-20][n][k][1]=procar.data[Spin.up][k][n][j][1]
                dot_size[j-20][n][k][2]=procar.data[Spin.up][k][n][j][3]