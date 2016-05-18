#!/bin/env python3

import re
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: {} <filename>".format(sys.argv[0]))
        return

    tags_re = re.compile(r'<\s*(\w[^/\s>]*)([^>]*?)/?>')

    attributes_re = r'''
        (\w[^\s=]*)
        \s*=\s*
        (?:
            ([\'"])(.*?)\2
            |
            ([^\s\'">]+)
        )
    '''
    attributes_re = re.compile(attributes_re, re.VERBOSE)

    with open(sys.argv[1], 'r') as f:
        for match in tags_re.findall(f.read()):
            tag, attributes = match

            print(tag)
            for match in attributes_re.findall(attributes):
                attribute = match[0]
                value = match[2] or match[3]

                print("\t{}={}".format(attribute, value))

if __name__ == '__main__':
    main()
