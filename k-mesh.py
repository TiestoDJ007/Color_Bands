# -*- coding: utf-8 -*-
import numpy as np

def y(x):
    y = -2 * x + 1
    return y


if __name__ == "__main__":
    G_x = 0.0
    G_y = 0.0
    M_x = 0.33
    M_y = 0.33
    K_x = 0.5
    K_y = 0.0
    step = 0.01

    Point_x_0 = np.arange(G_x, M_x + 0.01, step)
    k_mesh_part_0_list = []
    for i_0 in range(Point_x_0.size):
        x_0 = "%.4f" % Point_x_0[i_0]
        c_0 = np.arange(Point_x_0[i_0], M_x + 0.01, step)
        for j_0 in range(c_0.size):
            y_0 = "%.4f" % c_0[j_0]
            if y != '0.3400':
                k_mesh_part_0_list.append([float(x_0), float(y_0)])
    k_mesh_part_0 = np.array(k_mesh_part_0_list)

    Point_x_1 = np.arange(M_x + 0.01, K_x + 0.01, step)
    k_mesh_part_1_list = []
    for i_1 in range(Point_x_1.size):
        x_1 = "%.4f" % Point_x_1[i_1]
        f_1 = y(Point_x_1[i_1])
        c_1 = np.arange(0, f_1 + 0.01, 0.01)
        for j in range(c_1.size):
            y_1 = "%.4f" % c_1[j]
            k_mesh_part_1_list.append([float(x_1), float(y_1)])
    k_mesh_part_1 = np.array(k_mesh_part_1_list)
    k_mesh_part = np.concatenate((k_mesh_part_0, k_mesh_part_1), axis=0)
    k_mesh_part_3 = np.zeros(shape=(int(k_mesh_part.size / 2), 1))
    k_mesh_part_4 = np.ones(shape=(int(k_mesh_part.size / 2), 1))
    k_mesh = np.hstack((np.hstack((k_mesh_part, k_mesh_part_3)), k_mesh_part_4))

    out_file = open('KPOINTS', 'w')
    out_file.write("k-points for fermi-surface.\n")
    out_file.write("%d\n" % (k_mesh.shape[0]))
    out_file.write("Reciprocal\n")
    for i in range(np.shape(k_mesh)[0]):
        out_file.write("{0:4f} {1:4f} {2:4f} {3:0f}\n".format(float(k_mesh[i, 0]),
                                                              float(k_mesh[i, 1]),
                                                              float(k_mesh[i, 2]),
                                                              float(k_mesh[i, 3])))
    out_file.close()
    print("Done.")
