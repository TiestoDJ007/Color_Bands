# -*- coding: utf-8 -*-
#!/usr/bin/env python
from fractions import Fraction

#定义四条边界
def line1(x):
    return x


def line2(x):
    y = x
    return y


def line3(x):
    y = -2 * x + Fraction(1, 3)
    return y


def line4(x):
    y = -2 * x + Fraction(2, 3)

