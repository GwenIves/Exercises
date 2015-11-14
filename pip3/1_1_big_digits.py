#!/bin/env python3

import sys

ZERO = ["  ***  ", " *   * ", "*     *", "*     *", "*     *", " *   * ", "  ***  "]
ONE = [" * ", "** ", " * ", " * ", " * ", " * ", "***"]
TWO = [" *** ", "*   *", "*  * ", "  *  ", " *   ", "*    ", "*****"]
THREE = [" *** ", "*   *", "    *", "  ** ", "    *", "*   *", " *** "]
FOUR = ["   *  ", "  **  ", " * *  ", "*  *  ", "******", "   *  ", "   *  "]
FIVE = ["*****", "*    ", "*    ", " *** ", "    *", "*   *", " *** "]
SIX = [" *** ", "*    ", "*    ", "**** ", "*   *", "*   *", " *** "]
SEVEN = ["*****", "    *", "   * ", "  *  ", " *   ", "*    ", "*    "]
EIGHT = [" *** ", "*   *", "*   *", " *** ", "*   *", "*   *", " *** "]
NINE = [" ****", "*   *", "*   *", " ****", "    *", "    *", "    *"]

DIGITS_TEMPLATE = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

def get_digits():
    try:
        return [int(d) for d in sys.argv[1]]
    except IndexError:
        print("usage: {} <number>".format(sys.argv[0]))
    except ValueError as err:
        print(err, "in", sys.argv[1])

    return []

def get_digits_format(template):
    fmt = []

    for digit in range(len(template)):
        mapping = {ord('*') : str(digit)}

        fmt.append([s.translate(mapping) for s in template[digit]])

    return fmt


def main():
    num_digits = get_digits()

    if not num_digits:
        return

    digits = get_digits_format(DIGITS_TEMPLATE)

    for row in range(len(ZERO)):
        for column in range(len(num_digits)):
            print("{}  ".format(digits[num_digits[column]][row]), end="")

        print()

if __name__ == '__main__':
    main()
