#!/bin/env python3

# pylint: disable=bad-builtin,deprecated-lambda

import string

def is_ascii(s):
    return all(map(lambda c: ord(c) < 127, s))

def is_ascii_punctuation(s):
    return all(map(lambda c: c in string.punctuation, s))

def is_ascii_printable(s):
    return all(map(lambda c: c in string.printable, s))

def test():
    assert is_ascii("1235") is True
    assert is_ascii("1235\xaa") is False

    assert is_ascii_punctuation(",.;") is True
    assert is_ascii_punctuation("foo") is False

    assert is_ascii_printable("foo") is True
    assert is_ascii_printable("foo\xaa") is False

if __name__ == '__main__':
    test()
