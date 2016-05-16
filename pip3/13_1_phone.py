#!/bin/env python3

import re
import sys

def main():
    phone_re = r'''
        \s*
        (?:\((\d{3})\)|(\d{3}))
        [-\ ]?
        (\d{3})
        [-\ ]?
        (\d{4})
        \s*
    '''
    phone_re = re.compile(phone_re, re.VERBOSE)

    for line in sys.stdin:
        match = phone_re.match(line)

        if match is not None:
            mg = match.groups()
            print("({}) {} {}".format(mg[0] or mg[1], mg[2], mg[3]))
        else:
            print("Invalid phone number: {}".format(line.strip()))

if __name__ == '__main__':
    main()
