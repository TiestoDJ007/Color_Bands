# -*- coding: utf-8 -*-
# !/usr/bin/env python

from fractions import Fraction

import numpy as np


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getx(self):
        return self.x

    def gety(self):
        return self.y


class LineFunction:
    def __init__(self, x, p1, p2):
        self.k = Fraction(p2.gety() - p1.gety(), p2.getx() - p1.getx())
        self.b = p1.gety() - p1.getx() * Fraction(p2.gety() - p1.gety(),
                                                  p2.getx() - p1.getx())
        self.x = x

    def function(self):
        y = self.k * self.x + self.b
        return float(y)


if __name__ == "__main__":
    A = Point(Fraction(1, 6), 0)
    B = Point(Fraction(1, 3), 0)
    C = Point(Fraction(2, 9), Fraction(2, 9))
    D = Point(Fraction(1, 9), Fraction(1, 9))

    initial_points_ls = []
    a = np.linspace(0, 1, 500, endpoint=False)
    for i in range(len(a)):
        for j in range(len(a)):
            initial_points_ls.append(np.array((a[i], a[j])))
    initial_points = np.array(initial_points_ls)
    x = initial_points[:, 0]
    y = initial_points[:, 1]
    points = []
    for i in range(len(x)):
        xi = x[i]
        yi = y[i]
        if yi >= LineFunction(xi, A, B).function() and \
                yi >= LineFunction(xi, A, D).function() and \
                yi <= LineFunction(xi, C, B).function() and \
                yi <= LineFunction(xi, C, D).function():
            points.append(np.array((xi, yi)))

    fkp = open("KPOINTS", "w")
    fkp.write("Explicit k-points list")
    fkp.write("\n")
    fkp.write("{}".format(len(points)))
    fkp.write("\n")
    fkp.write("Reciprocal lattice")
    fkp.write("\n")
    for i in range(len(points)):
        fkp.write(
            "  {:.6f} {:.6f} {:.6f} {}".format(points[i][0], points[i][1], 0, 1))
        fkp.write('\n')