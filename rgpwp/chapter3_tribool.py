#!/bin/env python3

class Tribool(object):
    def __init__(self, val):
        if val is None:
            self.val = None
        else:
            self.val = bool(val)

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __bool__(self):
        return bool(self.val)

    def __invert__(self):
        if self.val is None:
            val = None
        else:
            val = not self.val

        return type(self)(val)

    def __and__(self, other):
        vals = (self.val, other.val)

        if False in vals:
            val = False
        elif None in vals:
            val = None
        else:
            val = True

        return type(self)(val)

    def __or__(self, other):
        vals = (self.val, other.val)

        if True in vals:
            val = True
        elif None in vals:
            val = None
        else:
            val = False

        return type(self)(val)

def test_tribool():
    t = Tribool(True)
    f = Tribool(False)
    u = Tribool(None)

    for tribool in (t, f, u):
        print("{!s}".format(tribool))
        print("{!r}".format(tribool))

    print()

    print(t == f)
    t2 = Tribool(True)
    print(t == t2)

    print()

    print(~t)
    print(~f)
    print(~u)

    print()

    for a in (t, f, u):
        for b in (t, f, u):
            print("{!s:<7} and {!s:^7} == {!s:>7}".format(a, b, a & b))

    print()

    for a in (t, f, u):
        for b in (t, f, u):
            print("{!s:<7} or {!s:^7} == {!s:>7}".format(a, b, a | b))

def main():
    test_tribool()

if __name__ == '__main__':
    main()
