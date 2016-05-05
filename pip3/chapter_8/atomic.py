#!/bin/env python3

import copy
import collections

class Atomic(object):
    def __init__(self, container, deep_copy=False):
        mutable_collections = (
            collections.MutableSequence,
            collections.MutableSet,
            collections.MutableMapping
        )

        if not isinstance(container, mutable_collections):
            raise ValueError("Not a mutable collection: %s" % (container.__class__.__name__))

        self.container = container
        self.orig = None
        self.deep_copy = deep_copy

    def __enter__(self):
        if self.deep_copy:
            self.orig = copy.deepcopy(self.container)
        else:
            self.orig = copy.copy(self.container)

        return self.container

    def __exit__(self, e_type, e_val, e_tb):
        if e_type is not None:
            if isinstance(self.container, collections.MutableSequence):
                self.container[:] = self.orig
            else:
                self.container.clear()
                self.container.update(self.orig)

def test():
    l = [1, 2, 3]
    try:
        with Atomic(l) as a:
            a[1] = 10
            a[2] = l[0]
    except Exception:
        pass
    assert l == [1, 10, 1]

    l = [1, 2, 3]
    try:
        with Atomic(l) as a:
            a[1] = 10
            a[2] = l[10]
    except Exception:
        pass
    assert l == [1, 2, 3]

    s = set([1, 2, 3])
    try:
        with Atomic(s) as a:
            a.add(10)
            a.remove(1)
    except Exception:
        pass
    assert s == set([10, 2, 3])

    s = set([1, 2, 3])
    try:
        with Atomic(s) as a:
            a.add(10)
            a.remove(4)
    except Exception:
        pass
    assert s == set([1, 2, 3])


if __name__ == '__main__':
    test()
