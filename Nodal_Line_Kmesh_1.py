# -*- coding: utf-8 -*-
# !/usr/bin/env python

from fractions import Fraction


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getx(self):
        return self.x

    def gety(self):
        return self.y


class LineFunc:
    def __init__(self, x, p1, p2):
        self.k = Fraction(p2.gety() - p1.gety(), p2.getx() - p1.getx())
        self.b = p1.gety() - p1.getx() * Fraction(p2.gety() - p1.gety(),
                                                  p2.getx() - p1.getx())
        self.x = x
        self.y = self.k * self.x + self.b

    def function(self):
        return float(self.y)


if __name__ == "__main__":
    A = Point(Fraction(1, 6), 0)
    B = Point(Fraction(1, 3), 0)
    C = Point(Fraction(1, 9), Fraction(1, 9))
    D = Point(Fraction(2, 9), Fraction(2, 9))

