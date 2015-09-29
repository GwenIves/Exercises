#!/bin/env python3

import cmath
import math
import sys

def get_float(msg, allow_zero):
    while True:
        try:
            x = float(input(msg))

            if allow_zero or abs(x) >= sys.float_info.epsilon:
                return x
            else:
                print("Zero not allowed")
        except ValueError as err:
            print(err)

def get_str(factor, variable):
    if abs(factor) < sys.float_info.epsilon:
        return ""
    elif factor > 0:
        return " + {}{}".format(factor, variable)
    else:
        return " - {}{}".format(-factor, variable)

def main():
    print("ax^2 + bx + c = 0")

    a = get_float("Enter a: ", False);
    b = get_float("Enter b: ", True);
    c = get_float("Enter c: ", True);

    D = b * b - 4 * a * c

    if abs(D) < sys.float_info.epsilon:
        x1 = -b / 2 * a
        x2 = None
    else:
        if D > 0:
            rD = math.sqrt(D)
        else:
            rD = cmath.sqrt(D)

        x1 =(-b + rD) / 2 * a
        x2 =(-b - rD) / 2 * a

    print()
    print("{}x^2{}{} = 0".format(a, get_str(b, "x"), get_str(c, "")))
    print()

    if not x2:
        print("Root: {}".format(x1))
    else:
        print("Root1: {}".format(x1))
        print("Root2: {}".format(x2))

if __name__ == '__main__':
    main()
