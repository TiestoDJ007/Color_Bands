# -*- coding: utf-8 -*-
# !/usr/bin/env python

import numpy as np
from matplotlib.path import Path

if __name__ == "__main__":
    A = np.array([0, 0])
    B = np.array([1 / 2, 0])
    C = np.array([1 / 3, 1 / 3])
    D = np.array([0, 1 / 2])
    # E = np.array([0, 1 / 6])
    # F = np.array([1 / 9, 1 / 9])

    initial_points_ls = []
    a = np.linspace(0, 1, 500, endpoint=False)
    for i in range(len(a)):
        for j in range(len(a)):
            initial_points_ls.append(np.array((a[i], a[j])))
    initial_points = np.array(initial_points_ls)

    point_path = [A, B, C, D, A]
    area = Path(point_path)
    kpoints = []
    for point in initial_points:
        if area.contains_point(point) == True:
            kpoints.append(point)
    kpoints = np.array(kpoints)

    kpoints_split = np.array_split(kpoints, 24, axis=0)

    for num_split in range(len(kpoints_split)):
        open_file = 'KPOINTS_split_part_{}'.format(num_split)
        fkp1 = open(open_file, "w")
        fkp1.write("Explicit k-points list")
        fkp1.write("\n")
        fkp1.write("{}".format(len(kpoints_split[num_split])))
        fkp1.write("\n")
        fkp1.write("Reciprocal lattice")
        fkp1.write("\n")
        for i in range(len(kpoints_split[num_split])):
            fkp1.write(
                "  {:.6f}  {:.6f}  {:.6f}  {}".format(kpoints_split[num_split][i][0],
                                                      kpoints_split[num_split][i][1],
                                                      0, 1))
            fkp1.write('\n')
        fkp1.close()
