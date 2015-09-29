#!/bin/env python3

import sys
import unicodedata

def matches_all(word, patterns):
    word = word.lower()

    for pattern in patterns:
        if not pattern in word:
            return False

    return True

def print_table(words):
    for i in range(len(words)):
        words[i] = words[i].lower()

    print("decimal   hex      chr {:^40}".format("name"))
    print("------- ----- -------- {}".format("-" * 40))

    for code in range(ord(" "), sys.maxunicode + 1):
        c = chr(code)

        try:
            name = unicodedata.name(c)
        except ValueError:
            continue

        if not words or matches_all(name, words):
            print("{0:7} {0:5X} {1!r:8} {2}".format(code, str(c), name.title()))

def main():
    print_table(sys.argv[1:])

if __name__ == '__main__':
    main()
