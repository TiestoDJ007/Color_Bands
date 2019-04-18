nx = 50
ny = 50
nz = 0

nkpt = (nx + 1) * (ny + 1) * (nz + 1)

fp2 = open("KPOINTS", "w")
fp2.write("Explicit k-points list")
fp2.write('\n')
fp2.write("{}".format(nkpt))
fp2.write('\n')
fp2.write("Reciprocal lattice")
fp2.write('\n')

for i in range(nx + 1):
    for j in range(ny + 1):
        fp2.write("  {:.6f}  {:.6f} {:.6f}  {}".format(i / nx, j / ny,0, 1))
        fp2.write('\n')
