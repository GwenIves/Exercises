#!/bin/env python3

class Stack(object):
    class EmptyStackError(Exception):
        pass

    def __init__(self, items=None):
        if items is None:
            self.list = []
        else:
            self.list = list(items)

    def pop(self):
        try:
            return self.list.pop()
        except IndexError:
            raise Stack.EmptyStackError

    def top(self):
        try:
            return self.list[-1]
        except IndexError:
            raise Stack.EmptyStackError

    def push(self, val):
        self.list.append(val)

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return str(self.list)

def test_stack():
    s = Stack(list(range(2)))
    s.push(7)
    s.push(20)

    print(len(s))
    print(s)
    print()

    print(s.top())
    print(s.top())
    print()

    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print()

    try:
        print(s.pop())
    except Stack.EmptyStackError:
        pass
    else:
        assert False, "Stack did not raise"

def main():
    test_stack()

if __name__ == '__main__':
    main()
